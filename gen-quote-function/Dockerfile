FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_genaiquote.py ${LAMBDA_TASK_ROOT}
COPY llm_helpers.py ${LAMBDA_TASK_ROOT}
COPY twitter.py ${LAMBDA_TASK_ROOT}
COPY config_loader.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_genaiquote.handler" ]
