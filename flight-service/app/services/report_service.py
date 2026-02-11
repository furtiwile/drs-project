from typing import List
from io import BytesIO
from datetime import datetime
from decimal import Decimal

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from app.domain.interfaces.services.report_service_interface import ReportServiceInterface
from app.domain.interfaces.repositories.ireport_repository import IReportRepository
from app.domain.models.flights import Flight
from app.utils.logger_service import get_logger, LoggerService

logger = get_logger(__name__)


class ReportService(ReportServiceInterface):
    """Service for generating PDF reports of flight data"""

    def __init__(self, report_repository: IReportRepository):
        self.report_repository = report_repository

    def generate_flight_report(self, report_types: List[str]) -> bytes:
        """
        Generate PDF report for specified flight report types.
        
        Args:
            report_types: List of report types to include ('upcoming', 'in_progress', 'completed')
            
        Returns:
            PDF file as bytes
        """
        LoggerService.log_service_call(logger, 'ReportService', 'generate_flight_report',
                                      report_types=report_types)

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.75*inch,
            bottomMargin=0.5*inch
        )

        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )

        # Report header
        title = Paragraph("Flight Management System Report", title_style)
        elements.append(title)
        
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        timestamp_text = Paragraph(f"<i>Generated on: {timestamp}</i>", styles['Normal'])
        elements.append(timestamp_text)
        elements.append(Spacer(1, 0.3*inch))

        # Generate sections based on requested report types
        for report_type in report_types:
            if report_type == 'upcoming':
                self._add_upcoming_section(elements, section_style, styles)
            elif report_type == 'in_progress':
                self._add_in_progress_section(elements, section_style, styles)
            elif report_type == 'completed':
                self._add_completed_section(elements, section_style, styles)

        # Build PDF
        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        LoggerService.log_with_context(logger, 'INFO', 'PDF report generated successfully',
                                      size_bytes=len(pdf_bytes),
                                      report_types=report_types)
        
        return pdf_bytes

    def _add_upcoming_section(self, elements, section_style, styles):
        """Add upcoming flights section to the report"""
        flights = self.report_repository.get_upcoming_flights()
        
        section_header = Paragraph("Upcoming Flights (Approved, Not Yet Departed)", section_style)
        elements.append(section_header)
        
        if not flights:
            no_data = Paragraph("<i>No upcoming flights found.</i>", styles['Normal'])
            elements.append(no_data)
            elements.append(Spacer(1, 0.3*inch))
            return
        
        # Create table data
        table_data = [
            ['Flight Name', 'Airline', 'Route', 'Departure', 'Arrival', 'Duration\n(min)', 
             'Distance\n(km)', 'Price', 'Total\nSeats', 'Created By']
        ]
        
        for flight in flights:
            route = f"{flight.departure_airport.code} → {flight.arrival_airport.code}"
            departure = flight.departure_time.strftime("%Y-%m-%d %H:%M")
            arrival = flight.arrival_time.strftime("%Y-%m-%d %H:%M")
            duration_minutes = int(flight.flight_duration.total_seconds() / 60)
            price = f"${float(flight.price):.2f}"
            
            table_data.append([
                flight.flight_name,
                flight.airline.name,
                route,
                departure,
                arrival,
                str(duration_minutes),
                str(flight.flight_distance_km),
                price,
                str(flight.total_seats),
                f"User {flight.created_by}"
            ])
        
        table = self._create_table(table_data)
        elements.append(table)
        
        # Summary
        total_revenue = sum(float(f.price) * f.total_seats for f in flights)
        summary = Paragraph(
            f"<b>Summary:</b> {len(flights)} upcoming flight(s), "
            f"Total potential revenue: ${total_revenue:,.2f}",
            styles['Normal']
        )
        elements.append(Spacer(1, 0.1*inch))
        elements.append(summary)
        elements.append(Spacer(1, 0.3*inch))

    def _add_in_progress_section(self, elements, section_style, styles):
        """Add in-progress flights section to the report"""
        flights = self.report_repository.get_in_progress_flights()
        
        section_header = Paragraph("In-Progress Flights (Currently Flying)", section_style)
        elements.append(section_header)
        
        if not flights:
            no_data = Paragraph("<i>No in-progress flights found.</i>", styles['Normal'])
            elements.append(no_data)
            elements.append(Spacer(1, 0.3*inch))
            return
        
        # Create table data
        table_data = [
            ['Flight Name', 'Airline', 'Route', 'Departed', 'Expected\nArrival', 
             'Duration\n(min)', 'Distance\n(km)', 'Price', 'Status']
        ]
        
        now = datetime.utcnow()
        for flight in flights:
            route = f"{flight.departure_airport.code} → {flight.arrival_airport.code}"
            departed = flight.actual_start_time.strftime("%Y-%m-%d %H:%M") if flight.actual_start_time else "N/A"
            arrival = flight.arrival_time.strftime("%Y-%m-%d %H:%M")
            duration_minutes = int(flight.flight_duration.total_seconds() / 60)
            price = f"${float(flight.price):.2f}"
            
            # Calculate elapsed time
            if flight.actual_start_time:
                elapsed = now - flight.actual_start_time
                elapsed_minutes = int(elapsed.total_seconds() / 60)
                remaining_minutes = max(0, duration_minutes - elapsed_minutes)
                status_text = f"{remaining_minutes}m remaining"
            else:
                status_text = "In Progress"
            
            table_data.append([
                flight.flight_name,
                flight.airline.name,
                route,
                departed,
                arrival,
                str(duration_minutes),
                str(flight.flight_distance_km),
                price,
                status_text
            ])
        
        table = self._create_table(table_data)
        elements.append(table)
        
        # Summary
        summary = Paragraph(f"<b>Summary:</b> {len(flights)} flight(s) currently in progress", styles['Normal'])
        elements.append(Spacer(1, 0.1*inch))
        elements.append(summary)
        elements.append(Spacer(1, 0.3*inch))

    def _add_completed_section(self, elements, section_style, styles):
        """Add completed/cancelled flights section to the report"""
        flights = self.report_repository.get_completed_flights()
        
        section_header = Paragraph("Completed & Cancelled Flights", section_style)
        elements.append(section_header)
        
        if not flights:
            no_data = Paragraph("<i>No completed or cancelled flights found.</i>", styles['Normal'])
            elements.append(no_data)
            elements.append(Spacer(1, 0.3*inch))
            return
        
        # Create table data
        table_data = [
            ['Flight Name', 'Airline', 'Route', 'Departure\nTime', 'Arrival\nTime',
             'Price', 'Status', 'Updated At']
        ]
        
        for flight in flights:
            route = f"{flight.departure_airport.code} → {flight.arrival_airport.code}"
            departure = flight.departure_time.strftime("%Y-%m-%d %H:%M")
            arrival = flight.arrival_time.strftime("%Y-%m-%d %H:%M")
            price = f"${float(flight.price):.2f}"
            status = flight.status.value
            updated = flight.updated_at.strftime("%Y-%m-%d %H:%M")
            
            table_data.append([
                flight.flight_name,
                flight.airline.name,
                route,
                departure,
                arrival,
                price,
                status,
                updated
            ])
        
        table = self._create_table(table_data)
        elements.append(table)
        
        # Summary
        completed_count = sum(1 for f in flights if f.status.value == 'COMPLETED')
        cancelled_count = sum(1 for f in flights if f.status.value == 'CANCELLED')
        completed_revenue = sum(float(f.price) * f.total_seats for f in flights if f.status.value == 'COMPLETED')
        
        summary = Paragraph(
            f"<b>Summary:</b> {completed_count} completed, {cancelled_count} cancelled | "
            f"Completed revenue: ${completed_revenue:,.2f}",
            styles['Normal']
        )
        elements.append(Spacer(1, 0.1*inch))
        elements.append(summary)
        elements.append(Spacer(1, 0.3*inch))

    def _create_table(self, data):
        """Create a styled table for flight data"""
        table = Table(data, repeatRows=1)
        
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.lightgrey]),
        ]))
        
        return table
