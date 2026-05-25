from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, JSON, Enum, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True, nullable = False)
    full_name = Column(String(100), nullable = False)
    email = Column(String(255), unique = True, index = True, nullable = False)
    hashed_password = Column(String, nullable = False)
    role = Column(Enum("candidate", "recruiter", name = "user_roles"), nullable = False)
    created_at = Column(DateTime(timezone = False), server_default = func.now(), nullable = False)
    updated_at = Column(DateTime(timezone = False), server_default = func.now(), onupdate = func.now(), nullable = False)
    is_active = Column(Boolean, default = True, nullable = False)

    candidate_profile = relationship("Candidate_Profiles", back_populates = "user", uselist = False)
    recruiter_profile = relationship("Recruiter_Profiles", back_populates = "user", uselist = False)


class Candidate_Profiles(Base):
    __tablename__ = 'candidate_profiles'

    id = Column(Integer, primary_key = True, index = True, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    phone = Column(String(20), unique = True)
    github_url = Column(String(255))
    linkedin_url = Column(String(255))
    portfolio_url = Column(String(255)) #optional
    experience_yrs = Column(Integer, default = 0)
    current_location = Column(String(100))
    created_at = Column(DateTime(timezone = False), server_default = func.now(), nullable = False)

    user = relationship("Users", back_populates = "candidate_profile")
    resumes = relationship("Resume", back_populates = "candidate")


class Recruiter_Profiles(Base):
    __tablename__ = 'recruiter_profiles'

    id = Column(Integer, primary_key = True, index = True, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    company_name = Column(String(255), nullable = False)
    designation = Column(String(100))
    created_at = Column(DateTime(timezone = False), server_default = func.now(), nullable = False)

    user = relationship("Users", back_populates = "recruiter_profile")
    jobs = relationship("Jobs", back_populates = "recruiter")


class Jobs(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key = True, index = True, nullable = False)
    recruiter_id = Column(Integer, ForeignKey("recruiter_profiles.id", ondelete = "CASCADE"), nullable = False)
    title = Column(String(255), nullable = False)
    description = Column(Text, nullable = False)
    required_skills = Column(JSON)
    required_experience = Column(Integer, default = 0)
    salary_range = Column(String(100))
    location = Column(String(100))
    employment_type = Column(String(50))
    is_active = Column(Boolean, default = True, nullable = False)
    created_at = Column(DateTime(timezone = False), server_default = func.now(), nullable = False)

    recruiter = relationship("Recruiter_Profiles", back_populates = "jobs")
    applications = relationship("Applications", back_populates = "job")


class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key = True, index = True, nullable = False)
    candidate_id = Column(Integer, ForeignKey("candidate_profiles.id", ondelete = "CASCADE"), nullable = False)
    file_url = Column(String, nullable = False)
    extracted_text = Column(Text)
    parsed_data = Column(JSON)
    resume_status = Column(Enum("pending", "processing", "completed", "failed", name = "resume_status_enum"), default = "pending", nullable = False)
    created_at = Column(DateTime(timezone = False), server_default = func.now(), nullable = False)
    updated_at = Column(DateTime(timezone = False), server_default = func.now(), onupdate = func.now(), nullable = False)

    candidate = relationship("Candidate_Profiles", back_populates = "resumes")
    applications = relationship("Applications", back_populates = "resume")


class Applications(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key = True, index = True, nullable = False)
    candidate_id = Column(Integer, ForeignKey("candidate_profiles.id", ondelete = "CASCADE"), nullable = False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete = "CASCADE"), nullable = False)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete = "CASCADE"), nullable = False)
    status = Column(Enum("applied", "shortlisted", "rejected", "hired", name = "application_status_enum"), default = "applied", nullable = False)
    applied_at = Column(DateTime(timezone = False), server_default = func.now(), nullable = False)

    job = relationship("Jobs", back_populates = "applications")
    resume = relationship("Resume", back_populates = "applications")
    ai_evaluation = relationship("AI_Evaluations", back_populates = "application", uselist = False)
    behavioral_assessment = relationship("Behavioral_Assessments", back_populates = "application", uselist = False)
    candidate = relationship("Candidate_Profiles")


class AI_Evaluations(Base):
    __tablename__ = "ai_evaluations"

    id = Column(Integer, primary_key = True, index = True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete = "CASCADE"), nullable = False)
    semantic_score = Column(Float)
    keyword_score = Column(Float)
    technical_score = Column(Float)
    overall_score = Column(Float)
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    recommendation = Column(Text)
    created_at = Column(DateTime(timezone = False), server_default = func.now(), nullable = False)

    application = relationship("Applications", back_populates = "ai_evaluation")


class Behavioral_Assessments(Base):
    __tablename__ = "behavioral_assessments"

    id = Column(Integer, primary_key = True, index = True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete = "CASCADE"), nullable = False)
    candidate_response = Column(Text)
    communication_score = Column(Float)
    accountability_score = Column(Float)
    problem_solving_score = Column(Float)
    adaptability_score = Column(Float)
    confidence_score = Column(Float)
    behavioral_score = Column(Float)
    overall_feedback = Column(Text)
    detailed_analysis = Column(JSON) 
    created_at = Column(DateTime(timezone = False), server_default = func.now(), nullable = False)

    application = relationship("Applications", back_populates = "behavioral_assessments")