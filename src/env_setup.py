import os
import sys

# Define the USD installation path
USD_INSTALL_PATH = '/opt/local/USD'


def setup_usd_environment(verbose=False):
    # Set environment variables
    os.environ['USD_INSTALL_ROOT'] = USD_INSTALL_PATH
    os.environ['PYTHONPATH'] = f"{USD_INSTALL_PATH}/lib/python:{os.environ.get('PYTHONPATH', '')}"
    os.environ['PATH'] = f"{USD_INSTALL_PATH}/bin:{os.environ.get('PATH', '')}"

    # Set DYLD_LIBRARY_PATH to include the USD library paths
    usd_lib_path = os.path.join(USD_INSTALL_PATH, 'lib')
    os.environ['DYLD_LIBRARY_PATH'] = f"{usd_lib_path}:{os.environ.get('DYLD_LIBRARY_PATH', '')}"

    # Manually append the USD Python library path
    usd_python_path = os.path.join(USD_INSTALL_PATH, 'lib', 'python')
    if usd_python_path not in sys.path:
        sys.path.append(usd_python_path)

    if verbose:
        # Print environment variables for debugging
        print(f"USD_INSTALL_ROOT: {os.environ['USD_INSTALL_ROOT']}")
        print(f"PYTHONPATH: {os.environ['PYTHONPATH']}")
        print(f"PATH: {os.environ['PATH']}")
        print(f"DYLD_LIBRARY_PATH: {os.environ['DYLD_LIBRARY_PATH']}")
        print(f"sys.path: {sys.path}")
