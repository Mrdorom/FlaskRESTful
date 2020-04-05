FROM python:3.6
MAINTAINER "1072274105@qq.com"
WORKDIR /home/work/FlaskRestful
# 表示把当前根目录下的所有文件复制到/home/work/app下面
COPY ./ ./
RUN pip install -r requirement.txt
EXPOSE 8888
# CMD /home/work/FlaskRestful/manager.py runserver --host 0.0.0.0 --port 8888
CMD ["python", "manager.py", "runserver", "--host", "0.0.0.0", "--port", "8888"]