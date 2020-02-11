from django.shortcuts import render
from django.views.generic import TemplateView , View
from django.http import HttpResponse , HttpResponseRedirect
from institute.models import Classs, Sessions, Programs, PhaseHasSession, Batches
from subjects.models import HasSubjects
from content.service import create_lectures

class LoginView(View):
    template_name = 'identity_service/login.html'
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class MainView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('dashboard')

class DashboardView(TemplateView):
    template_name = "identity_service/index.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class FacultyView(TemplateView):
    template_name = "identity_service/listing.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class FacultyAddViews(TemplateView):
    template_name = "identity_service/add.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class FacultyViewViews(TemplateView):
    pass
    # template_name = "identity_service/add.html"
    # def get(self, request, *args, **kwargs):
    #     context_data = {}
    #     return render(request, self.template_name, context_data)

class FacultyEditViews(TemplateView):
    template_name = "identity_service/update_faculty.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class StudentsViews(TemplateView):
    template_name = "identity_service/students.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class StudentsAddViews(TemplateView):
    template_name = "identity_service/add-student.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class StudentsViewViews(TemplateView):
    pass
    # template_name = "identity_service/add-student.html"
    # def get(self, request, *args, **kwargs):
    #     context_data = {}
    #     return render(request, self.template_name, context_data)

class StudentsEditViews(TemplateView):
    template_name = "identity_service/student_update.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class MasterSubjectsViews(TemplateView):
    template_name = "subjects/master-subject.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)



class SubjectsViews(TemplateView):
    template_name = "subjects/subjects.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class ClassViews(TemplateView):
    template_name = "institutes/class.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class ConceptsViews(TemplateView):
    template_name = "identity_service/concepts.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class SessionsViews(TemplateView):
    template_name = "institutes/session.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class ProgramsViews(TemplateView):
    template_name = "institutes/program.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class LecturePlannerView(TemplateView):
    template_name = "institutes/lecture-planner.html"
    def get_context_data(self):
        ctx = super(LecturePlannerView, self).get_context_data()
        ctx['classes'] = Classs.objects.all()
        ctx['subjects'] = HasSubjects.objects.all()
        ctx['sessions'] = Sessions.objects.all()
        ctx['programmes'] = Programs.objects.all()
        ctx['phases'] = PhaseHasSession.objects.all()
        ctx['batches'] = Batches.objects.all()
        return ctx

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        create_lectures(*args, **kwargs)
        return render(request, self.template_name, ctx)

class PhasesViews(TemplateView):
    template_name = "institutes/program-phases.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class BatchesViews(TemplateView):
    template_name = "institutes/program-batches.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class CentersViews(TemplateView):
    template_name = "identity_service/centers.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class DivisionsViews(TemplateView):
    template_name = "identity_service/division.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class DepartmentsViews(TemplateView):
    template_name = "identity_service/department.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class DesignationsViews(TemplateView):
    template_name = "identity_service/designation.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

class EmployementsViews(TemplateView):
    template_name = "identity_service/employment-type.html"
    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)
