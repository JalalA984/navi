FROM python:3.12-alpine

WORKDIR /navi

# Install required packages for Python and Node.js
RUN apk add --no-cache nodejs npm

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Ensure the shell script is executable
RUN chmod +x tw.sh
# Install TailwindCSS globally if needed
RUN npm install -g tailwindcss

EXPOSE 5000

CMD ["sh", "-c", "./tw.sh && python3 -m flask run --host=0.0.0.0"]