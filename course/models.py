from django.db import models
from django.utils import timezone
import uuid

class course(models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4,unique=True)
    Offering_Unit=models.CharField(max_length=100,default='')
    Offering_Department=models.CharField(max_length=100,default='')
    New_code=models.CharField(max_length=100,default='')
    Old_code=models.CharField(max_length=100,default='')
    courseTitleEng=models.CharField(max_length=100,default='')
    courseTitleChi=models.CharField(max_length=100,default='')
    Credits=models.CharField(max_length=100,default='')
    Course_Duration=models.CharField(max_length=100,default='')
    Medium_of_Instruction=models.CharField(max_length=100,default='')
    Teacher_Information=models.CharField(max_length=100,default='')

class course_noporf(models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4,unique=True)
    Offering_Unit = models.CharField(max_length=100, default='')  # 学院
    Offering_Department = models.CharField(max_length=100, default='')  # 院系
    New_code = models.CharField(max_length=100, default='')  # 新的课程编号，在对数据库检索时主要使用这一数据
    Old_code = models.CharField(max_length=100, default='')  # 旧的课程编号，新添加的课可能没用
    courseTitleEng = models.CharField(max_length=100, default='')  # 课程的英文名
    courseTitleChi = models.CharField(max_length=100, default='')  # 课程的中文名
    Credits = models.CharField(max_length=100, default='')  # 对应学分
    Course_Duration = models.CharField(max_length=100, default='')  # 课时？（大概）
    Medium_of_Instruction = models.CharField(max_length=100, default='')  # 授课语言

    def info(self): #调用本函数将会返回课程相关信息（无对应教师）
        content={
            "New_code":self.New_code,
            "Offering_Unit":self.Offering_Unit,
            "Old_code":self.Old_code,
            "courseTitleEng":self.courseTitleEng,
            "courseTitleChi":self.courseTitleChi,
            "Credits":float(self.Credits),
            "Medium_of_Instruction":self.Medium_of_Instruction,
            "Offering_Department":self.Offering_Department,
        }
        return content


class prof_info(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name=models.CharField(max_length=100)

    def info(self): #调用本函数将会返回教师相关信息
        content={
            "name":self.name
        }
        return content

class prof_with_course(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    prof=models.ForeignKey(prof_info,on_delete=models.CASCADE) #指向prof_info中的教师实例
    course=models.ForeignKey(course_noporf,on_delete=models.CASCADE) #指向course_noporf中的课程实例
    result=models.FloatField(default=0) # 本课程的综合评价
    comments=models.IntegerField(default=0) # 学生提交的评论总数
    attendance=models.FloatField(default=0.0) # 本课程的签到情况
    grade = models.FloatField(default=0.0) # 本课程的给分情况
    hard = models.FloatField(default=0.0) # 本课程的难易情况
    reward = models.FloatField(default=0.0) # 本课程的收获

    def info(self): #调用本函数将会返回课程相关信息（有对应教师）
        content={
            "name": self.prof.name,
            "result":self.result,
            "grade": self.grade,
            "attendance": self.attendance,
            "hard": self.hard,
            "reward": self.reward,
            "num":self.comments,
        }
        return content

class comment(models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    course=models.ForeignKey(prof_with_course,on_delete=models.CASCADE) #指向prof_with_course中的课程实例
    content=models.TextField() # 评价内容
    attendance=models.FloatField()# 本课程的签到情况
    pre=models.FloatField()#pre情况
    grade=models.FloatField()# 本课程的给分情况
    hard=models.FloatField()# 本课程的难易情况
    reward=models.FloatField()# 本课程的收获
    recommend=models.FloatField()# 是否推荐
    assignment=models.FloatField()# 作业情况
    result=models.FloatField(default=0) # 本次评价的综合得分
    pub_time=models.DateTimeField(default=timezone.now)# 提交时间

    def info(self): #调用本函数将会返回本次评价的相关信息
        content={
            "content": self.content,
            "grade": self.grade,
            "attendance": self.attendance,
            "hard": self.hard,
            "reward": self.reward,
            "pre": self.pre,
            "recommend": self.recommend,
            "assignment": self.assignment,
        }
        return content
