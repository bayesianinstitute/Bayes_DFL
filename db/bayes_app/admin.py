from django.contrib import admin
from bayes_app.models import TrainingInformation,TrainingResult,Logs,Admin,NodeStatus,GlobalModelHash,Track,TrainingResultAdmin



admin.site.register(TrainingInformation)
admin.site.register(TrainingResult)
admin.site.register(TrainingResultAdmin)
admin.site.register(Logs)
admin.site.register(Track)
admin.site.register(Admin)
admin.site.register(NodeStatus)
admin.site.register(GlobalModelHash)
