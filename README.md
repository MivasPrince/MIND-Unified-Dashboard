# 📊 MIND Unified Dashboard

A centralized analytics dashboard for Miva Open University's MIND platform, providing real-time insights for **Students**, **Faculty**, **Developers**, and **Administrators**.

Built with **Streamlit**, **Neon Postgres**, and modular analytics architecture.

---

## 🚀 Features

### Multi-Role Access
- **👨‍🎓 Student Dashboard**: Personal performance tracking, rubric feedback, engagement metrics
- **👩‍🏫 Faculty Dashboard**: Cohort analytics, at-risk student identification, rubric mastery analysis
- **👨‍💻 Developer Dashboard**: System health monitoring, API performance, environment quality metrics
- **🔧 Admin Dashboard**: Platform-wide KPIs, trends, cross-cutting analytics

### Key Capabilities
- 🔐 Role-based authentication and access control
- 📊 Interactive charts and visualizations (Plotly)
- 📈 Real-time performance analytics
- 📋 Detailed data tables with export functionality
- 🎨 Custom branded theme (light ash background, deep blue, red accents)
- 🗄 Optimized SQL queries for Neon Postgres
- 📱 Responsive layout for different screen sizes

---

## 📁 Project Structure

```plaintext
MIND-Unified-Dashboard/
├── Home.py                          # Main entry point
├── auth.py                          # Authentication module
├── db.py                            # Database connection manager
├── theme.py                         # Visual theme configuration
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── .streamlit/
│   └── secrets.toml                 # Database credentials (you must configure)
│
├── assets/
│   └── mind_logo.png               # Logo placeholder
│
├── pages/
│   ├── 1_Student_Dashboard.py      # Student analytics
│   ├── 2_Faculty_Dashboard.py      # Faculty/cohort analytics
│   ├── 3_Developer_Dashboard.py    # System health monitoring
│   └── 4_Admin_Dashboard.py        # Administrative KPIs
│
└── core/
    ├── components.py                # Reusable UI components
    ├── utils.py                     # Utility functions
    └── queries/
        ├── attempts_queries.py      # Attempts table queries
        ├── engagement_queries.py    # Engagement logs queries
        ├── environment_queries.py   # Environment & reliability queries
        ├── rubric_queries.py        # Rubric scores queries
        └── admin_queries.py         # Admin aggregates queries
```

---

## 🔧 Setup Instructions

### Prerequisites
- Python 3.9+
- Neon Postgres database (already set up with your schema)
- Git

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd MIND-Unified-Dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database Connection

Edit `.streamlit/secrets.toml` with your Neon Postgres credentials:

```toml
[database]
host = "your-project.neon.tech"          # Your Neon host
database = "mind_database"                # Your database name
user = "your_username"                    # Your username
password = "your_password"                # Your password
port = 5432
sslmode = "require"
```

**Important**: 
- Never commit `secrets.toml` to version control
- The file is already in `.gitignore`
- For deployment, use Streamlit Cloud secrets management

### 4. Run the Application

```bash
streamlit run Home.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## 🔐 Default Login Credentials

### Admin Access
- **Email**: `admin@example.com`
- **Password**: `admin123`

### Student Access
- **Email**: `student@example.com`
- **Password**: `student123`

### Faculty Access
- **Email**: `faculty@example.com`
- **Password**: `faculty123`

### Developer Access
- **Email**: `developer@example.com`
- **Password**: `dev123`

**⚠️ Security Note**: Change these credentials before deploying to production!

---

## 🎨 Theme Customization

The dashboard uses a custom color scheme defined in `theme.py`:

- **Background**: Light ash (#F5F5F5)
- **Primary**: Deep blue (#1B3B6F)
- **Secondary**: Medium blue (#2E5C8A)
- **Accent**: Crimson red (#DC143C)

To customize colors, edit `theme.py`:

```python
COLORS = {
    'background': '#F5F5F5',
    'primary': '#1B3B6F',
    'accent': '#DC143C',
    # ... other colors
}
```

---

## 📊 Dashboard Features by Role

### Student Dashboard
- **KPIs**: Cases attempted, average score, CES, time on task, active days, rubric mastery
- **Charts**: Score trend, improvement tracking, rubric mastery breakdown, engagement by action type
- **Tables**: Attempt history, rubric scores with feedback, engagement logs
- **Filters**: Date range, detailed view toggle

### Faculty Dashboard
- **KPIs**: Active students, class average, improvement rate, at-risk student count
- **Charts**: Score distribution by case, cohort comparison, rubric heatmap, engagement trends
- **Tables**: Student performance summary, at-risk students, rubric details
- **Filters**: Cohort, department, campus, case study, date range

### Developer Dashboard
- **KPIs**: System reliability index, API latency (p50/p95), error rates, environment quality
- **Charts**: Latency trends, error rates by API, environment impact on performance, device distribution
- **Tables**: System reliability logs, poor environment attempts, critical incidents
- **Filters**: Time range, API name, severity, device type, environment quality

### Admin Dashboard
- **KPIs**: Total active students, platform-wide averages, system health, cohort statistics
- **Charts**: Daily active users trend, usage by campus/department, case study engagement, weekly metrics
- **Tables**: Admin aggregates, top/bottom performing cohorts, incident summary
- **Filters**: Time range, campus, department, metric type

---

## 🗄 Database Schema

The dashboard connects to a Neon Postgres database with the following tables:

- **students**: Student profiles and cohort assignments
- **case_studies**: Case study definitions
- **attempts**: Student attempt records with scores
- **rubric_scores**: Detailed rubric assessments
- **engagement_logs**: User interaction tracking
- **environment_metrics**: Environment quality per attempt
- **system_reliability**: API performance monitoring
- **admin_aggregates**: Pre-computed platform metrics

See `schema.sql` for the complete schema definition.

---

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add database credentials in "Secrets" section
5. Deploy!

### Other Platforms

The application can be deployed on:
- Heroku
- AWS (EC2, ECS, Lambda)
- Google Cloud Run
- Azure App Service

Ensure you set environment variables for database connection.

---

## 🔧 Troubleshooting

### Database Connection Issues

**Error**: "Unable to connect to database"

**Solutions**:
1. Verify credentials in `.streamlit/secrets.toml`
2. Ensure Neon database is accessible
3. Check if IP is whitelisted in Neon dashboard
4. Verify SSL mode is set to "require"

### Import Errors

**Error**: "ModuleNotFoundError"

**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

### Port Already in Use

**Error**: "Port 8501 is already in use"

**Solution**:
```bash
streamlit run Home.py --server.port 8502
```

---

## 📝 Development

### Adding New Features

1. **New Query**: Add to appropriate file in `core/queries/`
2. **New Component**: Add to `core/components.py`
3. **New Dashboard Page**: Create in `pages/` following naming convention `N_PageName.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Document functions with docstrings
- Keep queries in separate query modules

### Testing

```bash
# Test database connection
python -c "from db import get_db_manager; db = get_db_manager(); print('✅ Connected' if db.test_connection() else '❌ Failed')"

# Run application
streamlit run Home.py
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is proprietary to Miva Open University.

---

## 📧 Support

For issues, questions, or feature requests:
- Create an issue in the GitHub repository
- Contact the development team
- Email: support@miva.university

---

## 🎯 Roadmap

- [ ] Real-time notifications for at-risk students
- [ ] Automated reporting and email summaries
- [ ] Mobile app version
- [ ] Advanced ML-based predictions
- [ ] Integration with LMS platforms
- [ ] Custom report builder
- [ ] Data export to multiple formats (PDF, Excel)

---

**Built with ❤️ for Miva Open University**

**Version**: 1.0.0  
**Last Updated**: November 2025
