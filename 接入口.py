import time

from fastapi import FastAPI, UploadFile
from typing import Union
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
