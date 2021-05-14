# DialoGPT
Web and service for conversation with RuDialoGPT

Article on Habr: https://habr.com/ru/company/icl_services/blog/548244/ 
# How it work
![Alt text](https://habrastorage.org/getpro/habr/upload_files/da2/3f6/b2f/da23f6b2fa158dd2a1773e5ed840e299.gif)
# Run
**Create environment:**
1. conda create -n rudialogpt python==3.7.9
2. conda activate rudialogpt
3. conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=10.2 -c pytorch
4. pip install transformers==4.4.2
5. pip install uvicorn==0.13.4
6. pip install Flask==1.1.2
7. pip install Flask-Bootstrap==3.3.7.1
8. pip install fastapi==0.63.0


**Run service:**
1. cd DialoGPT/src/service/
2. conda activate rudialogpt
3. python service.py

**Run web:**
1. cd DialoGPT/src/web/
2. conda activate rudialogpt
3. python app.py

By default service start on **localhost:8010**, web start on **localhost:8020**
