FROM python:3.8-alpine

COPY . /api
WORKDIR /api

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ENV FLASK_APP cafe_api.py
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]


# Second working approach - seems simpler method. However, in main.py -  app.run(debug=True, host='0.0.0.0', port=5001)
# EXPOSE 5001
# ENTRYPOINT [ "python" ]
# CMD [ "main.py"]