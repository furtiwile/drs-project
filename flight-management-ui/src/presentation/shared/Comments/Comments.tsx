import React, { useState, useEffect } from 'react';
import type { RatingResponse, RatingWithUserInfo } from '../../../domain/dtos/RatingDtos';
import { ratingService } from '../../../infrastructure/services/ratingService';
import { useToast } from '../../../application/context/ToastContext';
import { useAuth } from '../../../application/context/AuthContext';
import { useSocket } from '../../../application/context/SocketContext';
import { Role } from '../../../domain/enums/Role';
import './Comments.css';

interface CommentsProps {
  flightId: number;
  canAddComment?: boolean;
}

/**
 * Comments Component - Displays ratings/comments for flights
 * Follows Single Responsibility Principle - only manages comment display and creation
 * Uses dependency injection for services
 */
export const Comments: React.FC<CommentsProps> = ({
  flightId,
  canAddComment = false,
}) => {
  const [comments, setComments] = useState<RatingResponse[]>([]);
  const [adminComments, setAdminComments] = useState<RatingWithUserInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [newRating, setNewRating] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [error, setError] = useState<string | null>(null);

  const toast = useToast();
  const { user } = useAuth();
  const { on, off } = useSocket();

  useEffect(() => {
    loadComments();
    setupWebSocketListeners();

    return () => {
      off('rating_created');
      off('rating_updated');
      off('rating_deleted');
    };
  }, [flightId, currentPage]);

  const setupWebSocketListeners = () => {
    on('rating_created', (data: any) => {
      if (data.flight_id === flightId) {
        toast.info('New comment added to this flight');
        loadComments();
      }
    });

    on('rating_updated', (data: any) => {
      if (data.flight_id === flightId) {
        loadComments();
      }
    });

    on('rating_deleted', (data: any) => {
      if (data.flight_id === flightId) {
        loadComments();
      }
    });
  };

  const loadComments = async () => {
    setLoading(true);
    setError(null);
    try {
      let data;
      if (user?.role === Role.ADMINISTRATOR) {
        // Admins see all comments with user info
        data = await ratingService.getFlightRatings(flightId, currentPage, 10);
        setAdminComments(data.ratings as any);
      } else {
        // Regular users see basic comments
        data = await ratingService.getFlightRatings(flightId, currentPage, 10);
        setComments(data.ratings);
      }
      setTotalPages(data.pages);
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Failed to load comments';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleRatingChange = (rating: number) => {
    setNewRating(rating);
  };

  const handleSubmitRating = async () => {
    if (!user || newRating === 0) {
      toast.error('Please select a rating');
      return;
    }

    setSubmitting(true);
    try {
      await ratingService.createRating({
        flight_id: flightId,
        rating: newRating,
      });

      toast.success('Comment added successfully!');
      setNewRating(0);
      setCurrentPage(1);
      loadComments();
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Failed to add comment';
      toast.error(errorMessage);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteComment = async (commentId: number) => {
    if (!window.confirm('Are you sure you want to delete this comment?')) {
      return;
    }

    try {
      await ratingService.deleteRating(commentId);
      toast.success('Comment deleted successfully!');
      loadComments();
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Failed to delete comment';
      toast.error(errorMessage);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const renderStars = (rating: number) => {
    return (
      <div style={{ display: 'flex', gap: '2px', alignItems: 'center' }}>
        {[1, 2, 3, 4, 5].map((star) => (
          <span key={star} style={{ color: star <= rating ? '#ffc107' : '#ddd', fontSize: '16px' }}>
            ★
          </span>
        ))}
        <span className="rating-value">{rating}/5</span>
      </div>
    );
  };

  const displayedComments = user?.role === Role.ADMINISTRATOR ? adminComments : comments;

  return (
    <div className="comments-container">
      {/* Header */}
      <div className="comments-header">
        <h3 className="comments-title">Comments & Ratings</h3>
        <span className="comments-count">{displayedComments.length} Comment{displayedComments.length !== 1 ? 's' : ''}</span>
      </div>

      {/* Error Message */}
      {error && <div className="error-message">{error}</div>}

      {/* New Rating Section */}
      {canAddComment && user && (
        <div className="new-rating-section">
          <h4 style={{ margin: '0 0 15px 0', fontSize: '14px', fontWeight: '600' }}>
            Share your rating:
          </h4>
          <div className="rating-input-group">
            <div className="rating-stars">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  className={`star-button ${star <= newRating ? 'filled' : ''}`}
                  onClick={() => handleRatingChange(star)}
                  disabled={submitting}
                  type="button"
                >
                  ★
                </button>
              ))}
            </div>
            <span style={{ color: newRating > 0 ? '#ffc107' : '#ccc', fontWeight: '600' }}>
              {newRating > 0 ? `${newRating}/5` : 'Select rating'}
            </span>
            <button
              className="submit-rating-btn"
              onClick={handleSubmitRating}
              disabled={submitting || newRating === 0}
            >
              {submitting ? 'Submitting...' : 'Submit'}
            </button>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && <div className="loading-comments">Loading comments...</div>}

      {/* Comments List */}
      {!loading && displayedComments.length === 0 ? (
        <div className="no-comments">No comments yet. Be the first to rate this flight!</div>
      ) : (
        <>
          <div className="comments-list">
            {displayedComments.map((comment) => {
              const adminComment = comment as RatingWithUserInfo;
              const isOwnComment = user?.user_id === comment.user_id;

              return (
                <div key={comment.id} className="comment-item">
                  <div className="comment-content">
                    <div className="comment-header">
                      <span className="comment-user-info">
                        {adminComment.user_name || `User ${comment.user_id}`}
                        {user?.role === Role.ADMINISTRATOR && adminComment.user_email && (
                          <span style={{ fontSize: '12px', fontWeight: 'normal', color: '#6c757d' }}>
                            ({adminComment.user_email})
                          </span>
                        )}
                      </span>
                      <span className="comment-date">{formatDate(comment.created_at)}</span>
                    </div>
                    <div className="comment-rating">{renderStars(comment.rating)}</div>
                  </div>

                  {/* Actions for own comments or admin */}
                  {(isOwnComment || user?.role === Role.ADMINISTRATOR) && (
                    <div className="comment-actions">
                      {isOwnComment && (
                        <button
                          className="comment-action-btn delete"
                          onClick={() => handleDeleteComment(comment.id)}
                        >
                          Delete
                        </button>
                      )}
                      {user?.role === Role.ADMINISTRATOR && !isOwnComment && (
                        <button
                          className="comment-action-btn delete"
                          onClick={() => handleDeleteComment(comment.id)}
                        >
                          Remove
                        </button>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginTop: '15px' }}>
              <button
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
                style={{
                  padding: '6px 12px',
                  borderRadius: '4px',
                  border: '1px solid #dee2e6',
                  background: currentPage === 1 ? '#e9ecef' : 'white',
                  cursor: currentPage === 1 ? 'not-allowed' : 'pointer',
                }}
              >
                Previous
              </button>
              <span style={{ padding: '6px 12px', color: '#6c757d' }}>
                Page {currentPage} of {totalPages}
              </span>
              <button
                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
                style={{
                  padding: '6px 12px',
                  borderRadius: '4px',
                  border: '1px solid #dee2e6',
                  background: currentPage === totalPages ? '#e9ecef' : 'white',
                  cursor: currentPage === totalPages ? 'not-allowed' : 'pointer',
                }}
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Comments;
