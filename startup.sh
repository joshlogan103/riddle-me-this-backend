# Install TensorFlow if not already installed
if ! python -c "import tensorflow" &> /dev/null; then
    pip install tensorflow
fi

# Start the application
exec gunicorn Riddle_Me_This.wsgi --bind 0.0.0.0:$PORT

