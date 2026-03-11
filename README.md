# YouTube Channel Intelligence & Sentiment Analysis System

An AI-powered platform that analyzes **YouTube channel audience sentiment, engagement, and controversy patterns** using transformer-based NLP models and generative AI insights.

The system collects comments from recent videos of a channel, analyzes audience sentiment using a **fine-tuned MiniLM transformer model**, and generates **AI-driven insights and comparisons** between multiple creators.

---

# Project Overview

This project builds an **end-to-end AI analytics pipeline** that:

1. Collects channel data using **YouTube Data API v3**
2. Extracts **recent video comments**
3. Performs **transformer-based sentiment analysis**
4. Aggregates channel-level intelligence metrics
5. Generates **LLM-powered insights**
6. Displays results through an **interactive dashboard**

The system enables **real-time sentiment analysis and multi-channel comparison**, helping understand how audiences react to different creators.

---

# Key Features

## Channel Sentiment Analysis
Analyze audience reactions for any YouTube channel using recent video comments.

## Engagement Intelligence
Compute engagement scores using:

- likes
- views
- comment sentiment

## Controversy Detection
Measure how polarized audience reactions are based on comment sentiment distribution.

## Multi-Channel Comparison
Compare **up to 3 creators simultaneously** with ranked results based on:

- sentiment index
- engagement score
- controversy score

## AI-Generated Insights
Use **Groq LLM (Llama-3.1-8B)** to generate analytical summaries explaining:

- which channel performs best
- audience loyalty signals
- controversial content patterns
- viewer recommendations

## Interactive Dashboard
A **Streamlit frontend** allows users to analyze and compare channels in real time.

---

# System Architecture
User Interface (Streamlit)
│
▼
FastAPI Backend
│
├── YouTube API Service
│ • fetch channel videos
│ • retrieve video comments
│
├── Sentiment Analysis Service
│ • MiniLM transformer model
│ • comment sentiment classification
│
├── Aggregation Engine
│ • engagement score
│ • sentiment index
│ • controversy score
│
└── LLM Insight Engine
• Groq Llama-3.1-8B
• generates channel comparison insights

---

# Tech Stack

### Languages
Python

### Backend
FastAPI

### Frontend
Streamlit

### Machine Learning
Hugging Face Transformers  
MiniLM Transformer Model

### Data Processing
Pandas  
NumPy

### APIs
YouTube Data API v3  
Groq LLM API

### NLP
Transformer-based sentiment classification

---

# Project Structure
youtube-channel-intelligence
│
├── frontend
│ └── app.py
│
├── aggregation_service.py
├── sentiment.py
├── youtube_api.py
├── groq_service.py
├── gemini_service.py
├── main.py
│
├── minilm-twitter-sentiment
│ └── (fine-tuned sentiment model)
│
├── requirements.txt
└── README.md

---

# Core Metrics Generated

For each analyzed channel the system computes:

### Sentiment Index (0–100)
Overall audience positivity.

### Engagement Score
Normalized interaction level across recent videos.

### Controversy Score
Measures disagreement or polarized audience reactions.

### Sentiment Distribution
- Positive Ratio  
- Negative Ratio  
- Neutral Ratio  

---

# Example Output

### Channel Analysis
Sentiment Index: 73.88
Engagement Score: 0.032
Controversy Score: 0.372


### Channel Comparison


Mrwhosetheboss

MKBHD

JerryRigEverything


### AI Insights

- Identifies the strongest performing creator
- Detects audience loyalty signals
- Highlights controversial content patterns
- Provides viewer recommendations

---

# Model Details

The sentiment analysis component uses a **MiniLM transformer model fine-tuned on 800K+ social media comments** to improve understanding of informal language, slang, and emoji-heavy text common in YouTube comments.

Model performance:

- Validation F1 Score: **~72–83%**
- Optimized for **short social media text classification**

---

# Performance

| Task | Time |
|-----|-----|
Channel analysis | ~3–6 seconds |
LLM insight generation | ~1–2 seconds |
Comment processing | 80–400 comments per channel |

Batch inference improves transformer throughput by **~4× compared to naive inference**.

---

# Installation

### Clone the repository:

- git clone https://github.com/yourusername/youtube-channel-intelligence.git
- cd youtube-channel-intelligence

### Create virtual environment:

- python -m venv venv

### Activate environment:

- venv\Scripts\activate

### Install dependencies:

- pip install -r requirements.txt
- Environment Variables

## Set API keys before running

- YOUTUBE_API_KEY=your_youtube_api_key
- GROQ_API_KEY=your_groq_api_key

### Start backend:

- uvicorn main:app --reload

### Start frontend:

- streamlit run frontend/app.py

### Open in browser:

- http://localhost:8501


## Planned enhancements include:

- Natural language channel discovery using LLM agents

- Real-time trend detection

- Topic modeling for comment clusters

- Multi-genre channel recommendation engine

- Model deployment via Hugging Face Hub

## Use Cases

- Creator sentiment monitoring

- Audience feedback analysis

- Influencer performance comparison

- Content strategy insights

- Social media intelligence
