from django.http import HttpResponse

def view_record_event(request):
    from events.models import EventTracker

    category,action,label,email = ('','','','')

    if request.POST.has_key('category'):
        category = request.POST['category']

    if request.POST.has_key('action'):
        action = request.POST['action']

    if request.POST.has_key('label'):
        label = request.POST['label']

    if request.user.is_authenticated():
        email = request.user.email

    EventTracker.objects.create_event(email=email, category=category, action=action, label=label)

    return HttpResponse('True')

def view_bi_report(request,bi_report_template,**params):
    # A Report is identified by the id passed in the url for eg ?id=1 would fetch the report with id 1 from ReportingTools model                             
    # report_utils.py is the place where the default methods for all the reports are stored                                                                  
    # if a filter needs to be passed - pass it in the url like &filter=created_on__gte=2010-06-10 or any which way the program wishes to use                 
    # the filter                                                             
    from recordstory.models import ReportingTool

    # Call the default method as configured in the admin - use this method to return the result set in various forms like csv or graphs                      
    (rt,rcl,base_url) = ReportingTool.objects.get_results_and_headers(request)
    return response(bi_report_template, locals(), request)


def view_chart_data(request, show_graph_template):

     from libs import gviz_api
     from utils import _request_param_get
     from recordstory.models import ReportingTool
     from recordstory import report_utils

     columns = _request_param_get(request,'columns')
     (rt,rcl,base_url) = ReportingTool.objects.get_results_and_headers(request)

     graph_headers =  rt.graph_headers
     results = rcl.result_list

     (description,variables)=report_utils.created_description_for_annotated_time_graph(graph_headers)
     data_table = gviz_api.DataTable(description)

     from datetime import datetime
     for result in results:
         temp_dict = report_utils.create_data_table_for_annotated_time_graph(result, variables)
         data_table.AppendData( [temp_dict ])

     return HttpResponse(data_table.ToResponse(tqx=request.GET.get('tqx', '')))
