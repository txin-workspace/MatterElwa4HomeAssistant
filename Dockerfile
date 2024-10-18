ARG BUILD_FROM
FROM $BUILD_FROM

COPY ./source_code /matter_elwa
WORKDIR /matter_elwa
RUN apk add --no-cache python3 \
    && python3 -m venv venv \
    && . ./venv/bin/activate \
    && pip install -r requirements.txt \
    && chmod a+x run.sh

CMD [ "./run.sh" ]