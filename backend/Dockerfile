FROM python:3.9

# Δημιουργία χρήστη (απαραίτητο για το HF)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . /app

# ΠΡΟΣΟΧΗ: Port 7860 και app:app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]