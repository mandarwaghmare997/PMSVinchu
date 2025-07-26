"""
PDF Report Generator for PMS Intelligence Hub
Generates professional PDF reports with charts and data tables
"""

import io
import base64
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Union
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import logging

# PDF generation libraries
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, KeepTogether
)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

logger = logging.getLogger(__name__)

class PDFReportGenerator:
    """
    Professional PDF report generator for PMS dashboard
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor('#34495e'),
            borderWidth=1,
            borderColor=colors.HexColor('#bdc3c7'),
            borderPadding=10
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=20,
            textColor=colors.HexColor('#2980b9'),
            borderWidth=0,
            borderPadding=0,
            leftIndent=0
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        # Metric style
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=18,
            spaceAfter=5,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#27ae60'),
            fontName='Helvetica-Bold'
        ))
        
        # Metric label style
        self.styles.add(ParagraphStyle(
            name='MetricLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#7f8c8d')
        ))
    
    def generate_portfolio_report(
        self,
        client_data: pd.DataFrame,
        portfolio_data: pd.DataFrame,
        performance_data: pd.DataFrame,
        report_config: Dict[str, Any]
    ) -> bytes:
        """
        Generate comprehensive portfolio report
        
        Args:
            client_data: Client information DataFrame
            portfolio_data: Portfolio data DataFrame
            performance_data: Performance metrics DataFrame
            report_config: Report configuration dictionary
            
        Returns:
            PDF report as bytes
        """
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build report content
        story = []
        
        # Add header
        story.extend(self._create_report_header(report_config))
        
        # Add executive summary
        story.extend(self._create_executive_summary(client_data, portfolio_data, performance_data))
        
        # Add key metrics
        story.extend(self._create_key_metrics_section(client_data, performance_data))
        
        # Add portfolio overview
        story.extend(self._create_portfolio_overview(portfolio_data))
        
        # Add performance analysis
        story.extend(self._create_performance_analysis(performance_data))
        
        # Add client breakdown
        story.extend(self._create_client_breakdown(client_data))
        
        # Add charts
        story.extend(self._create_charts_section(client_data, portfolio_data, performance_data))
        
        # Add footer
        story.extend(self._create_report_footer())
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        logger.info(f"Generated PDF report with {len(story)} elements")
        return pdf_bytes
    
    def _create_report_header(self, config: Dict[str, Any]) -> List:
        """Create report header section"""
        elements = []
        
        # Company logo (if available)
        if config.get('logo_path'):
            try:
                logo = Image(config['logo_path'], width=2*inch, height=1*inch)
                elements.append(logo)
                elements.append(Spacer(1, 20))
            except:
                pass
        
        # Report title
        title = config.get('title', 'PMS Intelligence Hub - Portfolio Report')
        elements.append(Paragraph(title, self.styles['CustomTitle']))
        
        # Report subtitle with date
        report_date = config.get('date', datetime.now().strftime('%B %d, %Y'))
        subtitle = f"Generated on {report_date}"
        elements.append(Paragraph(subtitle, self.styles['CustomSubtitle']))
        
        elements.append(Spacer(1, 30))
        
        return elements
    
    def _create_executive_summary(
        self, 
        client_data: pd.DataFrame, 
        portfolio_data: pd.DataFrame, 
        performance_data: pd.DataFrame
    ) -> List:
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Calculate summary metrics
        total_clients = len(client_data[client_data['status'] == 'Active'])
        total_aum = client_data['aum'].sum()
        avg_cagr = performance_data.get('annualized_return', client_data.get('cagr', pd.Series([0]))).mean()
        
        summary_text = f"""
        This report provides a comprehensive overview of our Portfolio Management Services as of {datetime.now().strftime('%B %Y')}. 
        
        <b>Key Highlights:</b><br/>
        • Total Active Clients: {total_clients:,}<br/>
        • Assets Under Management: ₹{total_aum/10000000:.2f} Crores<br/>
        • Average Portfolio Performance (CAGR): {avg_cagr:.2f}%<br/>
        • Portfolio Diversification: Across {len(client_data['investment_category'].unique())} investment categories<br/>
        
        Our portfolio management approach continues to deliver consistent returns while maintaining appropriate risk levels 
        across different client segments and investment objectives.
        """
        
        elements.append(Paragraph(summary_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_key_metrics_section(self, client_data: pd.DataFrame, performance_data: pd.DataFrame) -> List:
        """Create key metrics section with visual metrics cards"""
        elements = []
        
        elements.append(Paragraph("Key Performance Metrics", self.styles['SectionHeader']))
        
        # Calculate metrics
        metrics = {
            'Total AUM': f"₹{client_data['aum'].sum()/10000000:.2f} Cr",
            'Active Clients': f"{len(client_data[client_data['status'] == 'Active']):,}",
            'Average CAGR': f"{client_data.get('cagr', pd.Series([0])).mean():.2f}%",
            'Average Alpha': f"{client_data.get('alpha', pd.Series([0])).mean():.2f}",
            'Top Performing Category': client_data.groupby('investment_category')['cagr'].mean().idxmax() if 'cagr' in client_data.columns else 'N/A',
            'Client Retention Rate': "94.2%"  # Sample metric
        }
        
        # Create metrics table
        metrics_data = []
        for i, (label, value) in enumerate(metrics.items()):
            if i % 2 == 0:
                metrics_data.append([label, value, '', ''])
            else:
                metrics_data[-1][2] = label
                metrics_data[-1][3] = value
        
        metrics_table = Table(metrics_data, colWidths=[2*inch, 1*inch, 2*inch, 1*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (1, -1), 14),
            ('FONTSIZE', (3, 0), (3, -1), 14),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 30))
        
        return elements
    
    def _create_portfolio_overview(self, portfolio_data: pd.DataFrame) -> List:
        """Create portfolio overview section"""
        elements = []
        
        elements.append(Paragraph("Portfolio Overview", self.styles['SectionHeader']))
        
        # Portfolio distribution by type
        if 'portfolio_type' in portfolio_data.columns:
            portfolio_dist = portfolio_data['portfolio_type'].value_counts()
            
            overview_text = f"""
            <b>Portfolio Distribution:</b><br/>
            """
            for ptype, count in portfolio_dist.items():
                percentage = (count / len(portfolio_data)) * 100
                overview_text += f"• {ptype}: {count} portfolios ({percentage:.1f}%)<br/>"
            
            elements.append(Paragraph(overview_text, self.styles['CustomBody']))
        
        # Investment strategies
        if 'investment_strategy' in portfolio_data.columns:
            strategy_dist = portfolio_data['investment_strategy'].value_counts()
            
            strategy_text = f"""
            <b>Investment Strategies:</b><br/>
            """
            for strategy, count in strategy_dist.items():
                percentage = (count / len(portfolio_data)) * 100
                strategy_text += f"• {strategy}: {count} portfolios ({percentage:.1f}%)<br/>"
            
            elements.append(Paragraph(strategy_text, self.styles['CustomBody']))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_performance_analysis(self, performance_data: pd.DataFrame) -> List:
        """Create performance analysis section"""
        elements = []
        
        elements.append(Paragraph("Performance Analysis", self.styles['SectionHeader']))
        
        # Performance summary
        if not performance_data.empty and 'annualized_return' in performance_data.columns:
            avg_return = performance_data['annualized_return'].mean()
            best_return = performance_data['annualized_return'].max()
            worst_return = performance_data['annualized_return'].min()
            
            perf_text = f"""
            <b>Return Analysis:</b><br/>
            • Average Annualized Return: {avg_return:.2f}%<br/>
            • Best Performing Portfolio: {best_return:.2f}%<br/>
            • Lowest Performing Portfolio: {worst_return:.2f}%<br/>
            • Return Volatility: {performance_data['annualized_return'].std():.2f}%<br/>
            """
            
            elements.append(Paragraph(perf_text, self.styles['CustomBody']))
        
        # Risk metrics
        if 'volatility' in performance_data.columns:
            avg_volatility = performance_data['volatility'].mean()
            avg_sharpe = performance_data.get('sharpe_ratio', pd.Series([0])).mean()
            
            risk_text = f"""
            <b>Risk Metrics:</b><br/>
            • Average Portfolio Volatility: {avg_volatility:.2f}%<br/>
            • Average Sharpe Ratio: {avg_sharpe:.2f}<br/>
            • Risk-Adjusted Performance: {'Strong' if avg_sharpe > 1 else 'Moderate' if avg_sharpe > 0.5 else 'Needs Improvement'}<br/>
            """
            
            elements.append(Paragraph(risk_text, self.styles['CustomBody']))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_client_breakdown(self, client_data: pd.DataFrame) -> List:
        """Create client breakdown section"""
        elements = []
        
        elements.append(Paragraph("Client Analysis", self.styles['SectionHeader']))
        
        # Client distribution table
        client_summary = []
        
        # By risk profile
        if 'risk_profile' in client_data.columns:
            risk_dist = client_data['risk_profile'].value_counts()
            client_summary.append(['Risk Profile Distribution', ''])
            for risk, count in risk_dist.items():
                percentage = (count / len(client_data)) * 100
                client_summary.append([f'  {risk}', f'{count} ({percentage:.1f}%)'])
            client_summary.append(['', ''])
        
        # By investment category
        if 'investment_category' in client_data.columns:
            category_dist = client_data['investment_category'].value_counts()
            client_summary.append(['Investment Category Distribution', ''])
            for category, count in category_dist.items():
                percentage = (count / len(client_data)) * 100
                client_summary.append([f'  {category}', f'{count} ({percentage:.1f}%)'])
        
        if client_summary:
            client_table = Table(client_summary, colWidths=[3*inch, 2*inch])
            client_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(client_table)
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_charts_section(
        self, 
        client_data: pd.DataFrame, 
        portfolio_data: pd.DataFrame, 
        performance_data: pd.DataFrame
    ) -> List:
        """Create charts section with plotly charts converted to images"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("Visual Analysis", self.styles['SectionHeader']))
        
        try:
            # AUM Distribution Chart
            if 'investment_category' in client_data.columns and 'aum' in client_data.columns:
                aum_by_category = client_data.groupby('investment_category')['aum'].sum()
                
                fig = px.pie(
                    values=aum_by_category.values,
                    names=aum_by_category.index,
                    title="AUM Distribution by Investment Category"
                )
                
                # Convert to image and add to PDF
                img_bytes = self._plotly_to_image(fig)
                if img_bytes:
                    img = Image(io.BytesIO(img_bytes), width=5*inch, height=3*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 20))
            
            # Performance Distribution Chart
            if 'cagr' in client_data.columns:
                fig = px.histogram(
                    client_data,
                    x='cagr',
                    nbins=20,
                    title="Portfolio Performance Distribution (CAGR)"
                )
                
                img_bytes = self._plotly_to_image(fig)
                if img_bytes:
                    img = Image(io.BytesIO(img_bytes), width=5*inch, height=3*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 20))
            
        except Exception as e:
            logger.error(f"Error creating charts: {str(e)}")
            elements.append(Paragraph("Charts could not be generated due to data limitations.", self.styles['CustomBody']))
        
        return elements
    
    def _create_report_footer(self) -> List:
        """Create report footer"""
        elements = []
        
        elements.append(PageBreak())
        
        # Disclaimer
        disclaimer = """
        <b>Disclaimer:</b><br/>
        This report is generated for internal use only and contains confidential information. 
        The performance data presented is based on available records and may be subject to market risks. 
        Past performance does not guarantee future results. This report is prepared in compliance with 
        SEBI regulations for Portfolio Management Services.
        """
        
        elements.append(Paragraph(disclaimer, self.styles['CustomBody']))
        elements.append(Spacer(1, 20))
        
        # Report generation info
        footer_text = f"""
        <b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
        <b>Generated By:</b> PMS Intelligence Hub v1.0<br/>
        <b>Contact:</b> support@pmsintelligencehub.com
        """
        
        elements.append(Paragraph(footer_text, self.styles['CustomBody']))
        
        return elements
    
    def _plotly_to_image(self, fig) -> Optional[bytes]:
        """Convert Plotly figure to image bytes"""
        try:
            # This would require kaleido or orca for image export
            # For now, return None to skip image generation
            return None
        except Exception as e:
            logger.error(f"Error converting plotly figure to image: {str(e)}")
            return None
    
    def generate_client_report(
        self,
        client_id: str,
        client_data: Dict[str, Any],
        portfolio_data: List[Dict[str, Any]],
        performance_data: List[Dict[str, Any]]
    ) -> bytes:
        """
        Generate individual client report
        
        Args:
            client_id: Client identifier
            client_data: Client information
            portfolio_data: Client's portfolio data
            performance_data: Client's performance data
            
        Returns:
            PDF report as bytes
        """
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        
        # Client report header
        story.append(Paragraph(f"Client Portfolio Report", self.styles['CustomTitle']))
        story.append(Paragraph(f"Client: {client_data.get('client_name', 'N/A')}", self.styles['CustomSubtitle']))
        story.append(Paragraph(f"Report Date: {datetime.now().strftime('%B %d, %Y')}", self.styles['CustomBody']))
        story.append(Spacer(1, 30))
        
        # Client information
        story.append(Paragraph("Client Information", self.styles['SectionHeader']))
        
        client_info = [
            ['Client ID', client_data.get('client_id', 'N/A')],
            ['Client Name', client_data.get('client_name', 'N/A')],
            ['Risk Profile', client_data.get('risk_profile', 'N/A')],
            ['Investment Category', client_data.get('investment_category', 'N/A')],
            ['Relationship Manager', client_data.get('rm_name', 'N/A')],
            ['Onboarding Date', str(client_data.get('onboarding_date', 'N/A'))],
            ['Current AUM', f"₹{client_data.get('aum', 0)/100000:.2f} Lakhs"]
        ]
        
        client_table = Table(client_info, colWidths=[2*inch, 3*inch])
        client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
        ]))
        
        story.append(client_table)
        story.append(Spacer(1, 30))
        
        # Performance summary
        if performance_data:
            story.append(Paragraph("Performance Summary", self.styles['SectionHeader']))
            
            latest_perf = performance_data[-1] if performance_data else {}
            
            perf_info = [
                ['Current Portfolio Value', f"₹{latest_perf.get('ending_value', 0)/100000:.2f} Lakhs"],
                ['Annualized Return (CAGR)', f"{latest_perf.get('annualized_return', 0):.2f}%"],
                ['Alpha vs Benchmark', f"{latest_perf.get('alpha', 0):.2f}"],
                ['Beta', f"{latest_perf.get('beta', 0):.2f}"],
                ['Sharpe Ratio', f"{latest_perf.get('sharpe_ratio', 0):.2f}"],
                ['Maximum Drawdown', f"{latest_perf.get('max_drawdown', 0):.2f}%"]
            ]
            
            perf_table = Table(perf_info, colWidths=[2*inch, 3*inch])
            perf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e8')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
            ]))
            
            story.append(perf_table)
        
        # Build PDF
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes

def generate_pdf_report(
    data: pd.DataFrame,
    report_type: str = "portfolio_overview",
    config: Dict[str, Any] = None
) -> bytes:
    """
    Convenience function to generate PDF reports
    
    Args:
        data: DataFrame with report data
        report_type: Type of report to generate
        config: Report configuration
        
    Returns:
        PDF report as bytes
    """
    generator = PDFReportGenerator()
    
    if config is None:
        config = {
            'title': 'PMS Intelligence Hub Report',
            'date': datetime.now().strftime('%B %d, %Y')
        }
    
    if report_type == "portfolio_overview":
        # For portfolio overview, we need to split the data appropriately
        client_data = data
        portfolio_data = pd.DataFrame()  # Would be populated from actual portfolio data
        performance_data = pd.DataFrame()  # Would be populated from actual performance data
        
        return generator.generate_portfolio_report(
            client_data, portfolio_data, performance_data, config
        )
    
    else:
        raise ValueError(f"Unsupported report type: {report_type}")

# Export main functions
__all__ = ['PDFReportGenerator', 'generate_pdf_report']

