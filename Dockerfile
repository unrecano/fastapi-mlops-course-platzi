FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV NLTK_DATA=/usr/share/nltk_data

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader -d /usr/share/nltk_data punkt punkt_tab stopwords wordnet averaged_perceptron_tagger averaged_perceptron_tagger_eng

COPY . .

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

