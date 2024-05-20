# Install TensorFlow if not already installed
if ! python -c "import tensorflow" &> /dev/null; then
    pip install tensorflow
fi

# Start the application
exec "$@"
