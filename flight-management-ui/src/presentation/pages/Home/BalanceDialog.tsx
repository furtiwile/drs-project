import { useState } from 'react';
import { userService } from '../../../infrastructure/services/userService';
import './BalanceDialog.css';

interface BalanceDialogProps {
  isOpen: boolean;
  currentBalance: number;
  onClose: () => void;
  onTransactionComplete: () => void;
}

export const BalanceDialog = ({ isOpen, currentBalance, onClose, onTransactionComplete }: BalanceDialogProps) => {
  const [amount, setAmount] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let value = e.target.value;
    
    // Remove any non-digit and non-dot characters
    value = value.replace(/[^\d.]/g, '');
    
    // Ensure only one dot
    const dotCount = (value.match(/\./g) || []).length;
    if (dotCount > 1) {
      value = value.substring(0, value.lastIndexOf('.'));
    }
    
    // Limit to 2 decimal places
    if (value.includes('.')) {
      const [integerPart, decimalPart] = value.split('.');
      value = integerPart + '.' + decimalPart.substring(0, 2);
    }
    
    setAmount(value);
  };

  const handleDeposit = async () => {
    if (!amount || parseFloat(amount) <= 0) {
      alert('Please enter a valid amount');
      return;
    }

    setIsLoading(true);
    try {
      await userService.deposit(parseFloat(amount));
      alert('Deposit successful!');
      setAmount('');
      onTransactionComplete();
      onClose();
    } catch {
      alert('Failed to deposit. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleWithdraw = async () => {
    if (!amount || parseFloat(amount) <= 0) {
      alert('Please enter a valid amount');
      return;
    }

    if (parseFloat(amount) > currentBalance) {
      alert('Insufficient balance for this withdrawal');
      return;
    }

    setIsLoading(true);
    try {
      await userService.withdraw(parseFloat(amount));
      alert('Withdrawal successful!');
      setAmount('');
      onTransactionComplete();
      onClose();
    } catch {
      alert('Failed to withdraw. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="balance-dialog-overlay" onClick={onClose}>
      <div className="balance-dialog" onClick={e => e.stopPropagation()}>
        <div className="dialog-header">
          <h2>Manage Balance</h2>
          <button className="close-btn" onClick={onClose}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div className="dialog-content">
          <div className="current-balance">
            <p className="label">Current Balance</p>
            <p className="amount">${currentBalance.toFixed(2)}</p>
          </div>

          <div className="input-group">
            <label htmlFor="amount">Amount (USD)</label>
            <input
              id="amount"
              type="text"
              inputMode="decimal"
              placeholder="0.00"
              value={amount}
              onChange={handleAmountChange}
              disabled={isLoading}
            />
          </div>

          <div className="dialog-actions">
            <button
              className="btn-withdraw"
              onClick={handleWithdraw}
              disabled={isLoading || !amount}
            >
              {isLoading ? 'Processing...' : 'Withdraw'}
            </button>
            <button
              className="btn-deposit"
              onClick={handleDeposit}
              disabled={isLoading || !amount}
            >
              {isLoading ? 'Processing...' : 'Deposit'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
