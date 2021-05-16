from django.db import models


class TestCase(models.Model):
    """
    测试用例表
    """
    service_id =models.IntegerField("服务id", null=False, db_index=True)
    name = models.CharField("名称", max_length=50, null=False)
    url = models.TextField("URL", null=False)
    method = models.IntegerField("请求方法", null=False, default=1) 
     # 1:GET, 2: POST, 3:PUT, 4:DELETE
    request_type = models.IntegerField("参数类型", null=False, default=1)  
    # 1：form-data 2: json
    request_body = models.TextField("参数内容")  # 必须要是一个json的格式数据
    # 格式无所谓
    
    response = models.TextField("结果")  # 这是用来展示用的，所以是一个文本
    response_assert = models.TextField("断言")   
    # 必须要是一个json的格式
    # {
    #     "关键字1": "include", 包含
    #     "关键字2": "exclude"  不包含
    # }

    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    def __str__(self):
        return self.name
