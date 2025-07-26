# PMS Intelligence Hub - Technical Architecture Document

**Author:** Manus AI  
**Date:** July 26, 2025  
**Version:** 1.0  
**Project:** Financial Dashboard for SEBI-Regulated PMS Entity

## Executive Summary

The PMS Intelligence Hub represents a comprehensive solution designed to automate data consolidation and reporting for SEBI-regulated Portfolio Management Services entities. This document outlines the technical architecture, implementation strategy, and deployment considerations for a system that integrates Salesforce CRM data with Wealth Spectrum PMS data to deliver real-time, interactive dashboards with advanced analytics capabilities.

The solution addresses the critical need to eliminate manual data consolidation processes while providing portfolio managers, relationship managers, and compliance officers with intuitive, filterable, and exportable views of client portfolios, performance metrics, and regulatory compliance data. Built with modern cloud-native technologies and designed for both AWS and on-premise deployment, the system ensures scalability, security, and compliance with SEBI regulations.

## Problem Statement and Business Context

Portfolio Management Services entities in India face significant operational challenges in data management and reporting. The current manual process of consolidating data from multiple systems creates inefficiencies, increases the risk of errors, and limits the ability to provide real-time insights to stakeholders. The typical workflow involves extracting data from Salesforce CRM systems, gathering portfolio and performance data from Wealth Spectrum platforms, and manually creating Management Information System (MIS) reports using spreadsheet applications.

This manual approach presents several critical issues. First, the time-intensive nature of data consolidation reduces the frequency of reporting and delays decision-making processes. Second, the potential for human error in data manipulation and calculation increases compliance risks in a heavily regulated industry. Third, the lack of real-time data access limits the ability to respond quickly to market changes or client needs. Finally, the absence of standardized reporting formats makes it difficult to maintain consistency across different time periods and client segments.

The regulatory environment in India, governed by the Securities and Exchange Board of India (SEBI), requires PMS entities to maintain detailed records of client portfolios, performance metrics, and compliance data. These requirements include regular reporting on Assets Under Management (AUM), performance calculations including Compound Annual Growth Rate (CAGR) and Extended Internal Rate of Return (XIRR), risk metrics such as Alpha and Beta, and detailed transaction histories. Manual processes make it challenging to ensure accuracy and timeliness in regulatory reporting while maintaining the audit trails required for compliance.

## Solution Architecture Overview

The PMS Intelligence Hub employs a modern, microservices-based architecture designed to handle the complex data integration and processing requirements of financial services organizations. The system follows a layered approach with clear separation of concerns, ensuring maintainability, scalability, and security.

The architecture consists of five primary layers: the Data Ingestion Layer, Data Processing and Storage Layer, Application Programming Interface (API) Layer, Presentation Layer, and Security and Compliance Layer. Each layer is designed to operate independently while maintaining seamless integration with adjacent layers through well-defined interfaces and protocols.

The Data Ingestion Layer serves as the entry point for all external data sources, including Salesforce CRM systems and Wealth Spectrum PMS platforms. This layer implements dual-mode connectivity, supporting both real-time API integration and batch processing of CSV/Excel files. The design ensures flexibility in data acquisition methods while maintaining data integrity and consistency across different source systems.

The Data Processing and Storage Layer transforms raw data into structured, analytics-ready formats. This layer implements Extract, Transform, Load (ETL) processes using Python-based frameworks, with data validation, cleansing, and normalization capabilities. The processed data is stored in a PostgreSQL database optimized for analytical queries, with optional integration to cloud-based data warehouses such as Google BigQuery for enhanced scalability.

The API Layer provides secure, RESTful endpoints for data access and manipulation. Built using FastAPI, this layer ensures high performance and automatic API documentation generation. The API design follows industry best practices for financial data security, including authentication, authorization, rate limiting, and comprehensive audit logging.

The Presentation Layer delivers an intuitive, interactive dashboard experience using Streamlit framework. This layer incorporates advanced visualization capabilities through Plotly charts, custom filtering and sorting mechanisms, and dynamic report generation. The user interface is designed to accommodate both technical and non-technical users, with role-based access controls and customizable views.

The Security and Compliance Layer encompasses all aspects of data protection, user authentication, and regulatory compliance. This layer implements encryption for data at rest and in transit, comprehensive audit logging, and compliance reporting capabilities aligned with SEBI requirements.

## Data Sources and Integration Strategy

The system integrates data from two primary sources: Salesforce CRM and Wealth Spectrum PMS platforms. Each source provides distinct but complementary data sets that, when combined, create a comprehensive view of client relationships and portfolio performance.

Salesforce CRM integration focuses on client relationship data, including client demographics, contact information, relationship manager assignments, onboarding dates, and communication histories. The system supports both Salesforce REST API integration for real-time data access and CSV export processing for batch updates. The REST API integration utilizes OAuth 2.0 authentication and implements rate limiting to comply with Salesforce API usage policies. For organizations preferring batch processing, the system can automatically process CSV exports placed in designated directories or received via email attachments.

The Salesforce integration captures critical business metrics including client acquisition trends, relationship manager performance, and client lifecycle management data. This information is essential for business development analysis, client retention strategies, and regulatory reporting requirements. The system maintains historical data to support trend analysis and performance tracking over extended periods.

Wealth Spectrum PMS integration provides comprehensive portfolio and performance data, including current holdings, historical transactions, Net Asset Value (NAV) calculations, performance metrics, and benchmark comparisons. Similar to Salesforce integration, the system supports both API-based real-time integration and file-based batch processing. The API integration maintains secure connections using authentication tokens and implements data validation to ensure accuracy of financial calculations.

The Wealth Spectrum integration captures detailed portfolio analytics including asset allocation breakdowns, sector and geographic diversification metrics, risk-adjusted performance measures, and compliance monitoring data. This information supports portfolio management decisions, client reporting requirements, and regulatory compliance obligations. The system maintains transaction-level detail to support audit requirements and performance attribution analysis.

Data synchronization between sources is managed through a sophisticated ETL pipeline that identifies and resolves data conflicts, maintains referential integrity, and ensures consistency across time periods. The system implements change data capture mechanisms to identify incremental updates and minimize processing overhead during regular synchronization cycles.

## Database Design and Data Modeling

The database design follows a star schema approach optimized for analytical queries while maintaining transactional integrity for operational processes. The central fact tables store quantitative measures such as portfolio values, transaction amounts, and performance metrics, while dimension tables provide descriptive attributes for clients, portfolios, time periods, and asset categories.

The Client dimension table serves as the primary entity for all client-related information, including unique client identifiers, demographic data, risk profiles, and relationship manager assignments. This table maintains historical records to support client lifecycle analysis and regulatory reporting requirements. The design accommodates complex client structures including individual accounts, family offices, and institutional clients with multiple sub-accounts.

The Portfolio dimension table captures portfolio-level attributes including investment strategies, benchmark assignments, fee structures, and inception dates. This table supports multiple portfolio structures per client and maintains relationships to underlying asset holdings. The design enables portfolio-level performance analysis and supports complex reporting requirements for different investment strategies and time periods.

The Time dimension table provides comprehensive date and time attributes to support various analytical requirements including calendar year analysis, financial year reporting, and custom date range queries. This table includes business day calculations, holiday adjustments, and period-end markers essential for accurate performance calculations and regulatory reporting.

The Asset dimension table maintains detailed information about individual securities, mutual funds, and other investment instruments. This table includes security identifiers, classification codes, sector assignments, and market data integration points. The design supports complex asset hierarchies and enables detailed portfolio attribution analysis.

The Transaction fact table records all portfolio transactions including purchases, sales, dividend receipts, and fee payments. This table maintains transaction-level detail necessary for accurate performance calculations and audit trail requirements. The design supports complex transaction types including corporate actions, stock splits, and merger events.

The Performance fact table stores calculated performance metrics at various aggregation levels including daily, monthly, quarterly, and annual periods. This table includes returns calculations, risk metrics, and benchmark comparisons. The design enables efficient query performance for dashboard displays while maintaining calculation transparency for audit purposes.

The database implements comprehensive indexing strategies to optimize query performance for dashboard operations. Composite indexes support common filtering combinations including client, date range, and portfolio type queries. The design includes materialized views for frequently accessed aggregations and implements automated maintenance procedures to ensure optimal performance.

## Application Programming Interface (API) Design

The API layer provides a comprehensive set of RESTful endpoints designed to support all dashboard functionality while maintaining security and performance standards appropriate for financial data systems. The API design follows OpenAPI 3.0 specifications and implements automatic documentation generation through FastAPI's built-in capabilities.

Authentication and authorization are implemented using JSON Web Tokens (JWT) with role-based access controls. The system supports multiple authentication methods including username/password combinations, single sign-on integration, and API key authentication for system-to-system communications. Role definitions include Portfolio Manager, Relationship Manager, Compliance Officer, and System Administrator, each with appropriate data access permissions and functional capabilities.

The Client Management endpoints provide comprehensive access to client data including profile information, portfolio assignments, and relationship histories. These endpoints support complex filtering and sorting operations to enable efficient data retrieval for dashboard displays. The design includes pagination support for large client lists and implements caching mechanisms to optimize performance for frequently accessed data.

The Portfolio Data endpoints deliver detailed portfolio information including current holdings, historical performance, and transaction histories. These endpoints support multiple aggregation levels and time period selections to accommodate various reporting requirements. The design includes real-time calculation capabilities for performance metrics and implements data validation to ensure accuracy of financial calculations.

The Performance Analytics endpoints provide access to calculated performance metrics including returns, risk measures, and benchmark comparisons. These endpoints support custom date range selections and multiple calculation methodologies to accommodate different reporting standards. The design includes attribution analysis capabilities and implements performance calculation transparency for audit requirements.

The Dashboard Configuration endpoints enable users to save and retrieve custom dashboard views, filter combinations, and report templates. These endpoints support user-specific configurations and implement sharing capabilities for collaborative analysis. The design includes version control for saved configurations and implements backup and recovery procedures for user preferences.

The Report Generation endpoints provide PDF export capabilities with customizable templates and branding options. These endpoints support batch report generation and implement queuing mechanisms for resource-intensive operations. The design includes template management capabilities and implements compliance features such as regulatory disclaimers and audit trail documentation.

## User Interface and Experience Design

The user interface design prioritizes intuitive navigation and efficient data access while accommodating the complex analytical requirements of financial professionals. The design employs a responsive layout that adapts to different screen sizes and device types, ensuring accessibility across desktop, tablet, and mobile platforms.

The main dashboard provides an executive summary view with key performance indicators, portfolio summaries, and alert notifications. This view implements dynamic data visualization using Plotly charts with interactive capabilities including drill-down functionality, zoom controls, and data point tooltips. The design includes customizable widget arrangements and implements user preference storage for personalized dashboard layouts.

The Client Analytics section provides detailed client-level analysis with comprehensive filtering and sorting capabilities. Users can filter by Assets Under Management ranges, performance metrics, investment categories, risk profiles, and time periods. The interface implements advanced search functionality with auto-complete suggestions and supports saved search configurations for frequently used filter combinations.

The Portfolio Performance section delivers detailed portfolio analysis with time-series charts, benchmark comparisons, and risk-return scatter plots. The interface supports multiple chart types including line charts, bar charts, heat maps, and correlation matrices. Users can customize chart parameters, export chart images, and create comparative analysis across multiple portfolios or time periods.

The Compliance and Reporting section provides access to regulatory reports, compliance monitoring dashboards, and audit trail information. The interface implements role-based access controls to ensure appropriate data visibility and includes workflow management capabilities for report approval processes. Users can schedule automated report generation and configure alert notifications for compliance threshold breaches.

The interface incorporates advanced animation effects using anime.js to enhance user engagement and provide visual feedback during data loading and transition operations. These animations include smooth page transitions, progressive data loading indicators, and interactive element highlighting. The design ensures animations enhance rather than distract from the analytical workflow while maintaining professional appearance standards appropriate for financial applications.

The PDF export functionality provides comprehensive report generation capabilities with customizable templates, branding options, and compliance features. Users can generate reports for individual clients, portfolio groups, or custom data selections. The export process includes progress indicators, preview capabilities, and automated email delivery options for report distribution.

## Security Architecture and Compliance Framework

The security architecture implements multiple layers of protection designed to meet the stringent requirements of financial services organizations while ensuring compliance with SEBI regulations and industry best practices. The framework addresses data protection, access control, audit logging, and incident response capabilities.

Data encryption is implemented at multiple levels including encryption at rest using AES-256 encryption for database storage and file systems, and encryption in transit using TLS 1.3 for all network communications. The system implements key management procedures with regular key rotation schedules and secure key storage using hardware security modules or cloud-based key management services.

Access control mechanisms implement the principle of least privilege with role-based permissions and multi-factor authentication requirements. The system maintains detailed user access logs and implements automated account lockout procedures for suspicious activity. Password policies enforce complexity requirements and regular password changes, while session management implements timeout controls and concurrent session limitations.

The audit logging framework captures comprehensive activity records including user authentication events, data access operations, configuration changes, and system administration activities. Audit logs are stored in tamper-evident formats with digital signatures and implement automated backup procedures to ensure availability for regulatory examinations. The system provides audit trail reporting capabilities with search and filtering functions to support compliance investigations.

Network security controls implement firewall configurations, intrusion detection systems, and network segmentation to protect against external threats. The system includes vulnerability scanning procedures, security patch management processes, and incident response protocols. Regular security assessments and penetration testing ensure ongoing protection effectiveness.

Data privacy controls implement data masking procedures for non-production environments, personal data protection measures, and data retention policies aligned with regulatory requirements. The system includes data classification procedures and implements appropriate handling controls for different data sensitivity levels.

Compliance monitoring capabilities include automated compliance checking, regulatory reporting functions, and exception management procedures. The system maintains compliance documentation and implements change management procedures to ensure ongoing regulatory adherence. Regular compliance assessments and regulatory update monitoring ensure continued alignment with evolving requirements.

## Deployment Architecture and Infrastructure

The deployment architecture supports both cloud-based and on-premise installations with containerized applications and automated deployment procedures. The design prioritizes scalability, availability, and maintainability while optimizing costs and resource utilization.

The cloud deployment option utilizes Amazon Web Services (AWS) infrastructure with services selected to remain within free tier limits where possible while ensuring production-ready capabilities. The architecture employs AWS Elastic Container Service (ECS) for application hosting with auto-scaling capabilities based on resource utilization and user demand. The database layer utilizes Amazon Relational Database Service (RDS) with PostgreSQL engine, implementing automated backup procedures and multi-availability zone deployment for high availability.

The application layer implements load balancing using AWS Application Load Balancer with health check monitoring and automatic failover capabilities. The system utilizes Amazon CloudFront for content delivery and implements AWS Certificate Manager for SSL certificate management. Storage requirements are met using Amazon S3 for file storage and backup retention with lifecycle policies for cost optimization.

The on-premise deployment option utilizes Docker containerization with Docker Compose orchestration for simplified deployment and management. The architecture includes database containers with persistent volume management and implements backup and recovery procedures using standard database tools. The system includes monitoring and logging capabilities using open-source tools such as Prometheus and Grafana.

Both deployment options implement continuous integration and continuous deployment (CI/CD) pipelines using GitHub Actions with automated testing, security scanning, and deployment procedures. The pipelines include environment promotion workflows with approval gates and implement rollback capabilities for rapid recovery from deployment issues.

Monitoring and alerting capabilities include application performance monitoring, resource utilization tracking, and error rate monitoring. The system implements automated alert notifications for critical issues and includes dashboard displays for operational metrics. Log aggregation and analysis capabilities support troubleshooting and performance optimization activities.

Backup and disaster recovery procedures include automated database backups, application configuration backups, and user data protection. The system implements recovery time objectives and recovery point objectives appropriate for financial services operations and includes regular disaster recovery testing procedures.

## Performance Optimization and Scalability

The system architecture implements multiple performance optimization strategies designed to ensure responsive user experiences while supporting growth in data volumes and user populations. The optimization approach addresses database performance, application efficiency, and user interface responsiveness.

Database optimization includes comprehensive indexing strategies with composite indexes for common query patterns and partial indexes for filtered queries. The system implements query optimization procedures with execution plan analysis and includes database maintenance procedures such as statistics updates and index reorganization. Materialized views provide pre-calculated aggregations for frequently accessed data and implement automated refresh procedures to maintain data currency.

Application-level caching implements multiple cache layers including in-memory caching for frequently accessed data, Redis caching for session data and temporary calculations, and content delivery network caching for static assets. The caching strategy includes cache invalidation procedures to ensure data consistency and implements cache warming procedures for optimal performance during peak usage periods.

The user interface implements progressive loading techniques with skeleton screens during data loading operations and implements lazy loading for large data sets. Chart rendering optimization includes data sampling for large time series and implements interactive zoom capabilities for detailed analysis. The interface includes performance monitoring with user experience metrics tracking and implements optimization procedures based on usage patterns.

Scalability planning includes horizontal scaling capabilities for application servers and implements database scaling strategies including read replicas for query distribution. The system includes capacity planning procedures with growth projections and implements resource monitoring with automated scaling triggers. Load testing procedures ensure performance under peak usage conditions and include stress testing for system limits identification.

## Integration and Extensibility Framework

The system architecture provides comprehensive integration capabilities designed to accommodate future expansion and third-party system connectivity. The integration framework implements standardized interfaces and protocols while maintaining security and data integrity requirements.

API integration capabilities include RESTful API endpoints for external system connectivity and implement webhook support for real-time event notifications. The system includes API rate limiting and authentication procedures and implements comprehensive API documentation with code examples and testing tools. Integration monitoring includes API usage tracking and error rate monitoring with automated alert notifications for integration issues.

Data import and export capabilities support multiple file formats including CSV, Excel, JSON, and XML with automated data validation and error handling procedures. The system includes batch processing capabilities for large data volumes and implements scheduling procedures for automated data synchronization. Export capabilities include custom report generation with template management and automated distribution procedures.

Third-party service integration includes market data providers, benchmark data sources, and regulatory reporting systems. The system implements secure connectivity procedures with authentication and encryption requirements and includes data validation procedures to ensure accuracy and completeness. Integration testing procedures ensure ongoing connectivity and data quality.

The extensibility framework includes plugin architecture for custom functionality development and implements configuration management procedures for system customization. The system includes development tools and documentation for custom extension creation and implements testing procedures for custom functionality validation.

## Conclusion and Implementation Roadmap

The PMS Intelligence Hub represents a comprehensive solution for automating financial data management and reporting in SEBI-regulated Portfolio Management Services organizations. The architecture provides the scalability, security, and functionality required to support modern financial services operations while ensuring regulatory compliance and operational efficiency.

The implementation roadmap prioritizes rapid deployment of core functionality while establishing the foundation for future enhancements and expansion. The phased approach ensures early value delivery while minimizing implementation risks and resource requirements. The system design accommodates both immediate operational needs and long-term strategic objectives, providing a platform for continued innovation and growth.

The technical architecture ensures maintainability and extensibility while implementing industry best practices for security, performance, and compliance. The deployment options provide flexibility for different organizational requirements while maintaining consistent functionality and user experiences across different environments.

The successful implementation of this system will eliminate manual data consolidation processes, improve reporting accuracy and timeliness, enhance decision-making capabilities, and ensure regulatory compliance. The investment in modern technology infrastructure will provide long-term benefits through improved operational efficiency, reduced compliance risks, and enhanced client service capabilities.

## References

[1] Securities and Exchange Board of India. "Portfolio Management Services Regulations." https://www.sebi.gov.in/legal/regulations/portfolio-management-services-regulations.html

[2] Salesforce Developer Documentation. "REST API Developer Guide." https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/

[3] Amazon Web Services. "Well-Architected Framework." https://aws.amazon.com/architecture/well-architected/

[4] FastAPI Documentation. "FastAPI Framework, High Performance, Easy to Learn." https://fastapi.tiangolo.com/

[5] Streamlit Documentation. "The Fastest Way to Build and Share Data Apps." https://docs.streamlit.io/

[6] PostgreSQL Documentation. "PostgreSQL: The World's Most Advanced Open Source Relational Database." https://www.postgresql.org/docs/

[7] Plotly Documentation. "Plotly Python Graphing Library." https://plotly.com/python/

[8] Docker Documentation. "Docker: Accelerated Container Application Development." https://docs.docker.com/

