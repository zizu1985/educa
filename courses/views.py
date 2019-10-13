from django.views.generic.list import ListView
from .models import Course
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, \
                                        DeleteView
from braces.views import LoginRequiredMixin, \
                         PermissionRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.shortcuts import get_object_or_404, redirect
from django.apps import apps
from django.forms.models import modelform_factory
from .models import Module, Content
from django.http import HttpResponseNotFound
from django.db.models import Count
from .models import Subject
from django.views.generic.detail import DetailView
from students.forms import CourseEnrollForm

# Uzytkwonik widzi tylko swoje dziela
class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


# Przy walidacji formy dostaje ona ownera
# Waliduj -> zapisz -> wlascicielem jest owner
class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


# Modele o ktorym mowimy jest Course
# Uzytkowin widzi tylko kursy ktorych jest ownerem
class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


# Widok - kursy
# Przy zapisie uzytkownik staje sie wlascicielem tego co stworzyl
class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject','title','slug','overview']
    # reverse, bo url brany z urls.py.
    # mapowanie view -> url
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'


# Widzi tylko swoje.
class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    #template_name = 'courses/manage/course/form.html'
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    template_name = 'courses/manage/course/form.html'
    permission_required = 'courses.change_course'


class CourseDeleteView( PermissionRequiredMixin,
                        OwnerCourseMixin,
                        DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    # set formset for view
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,
                             data=data)

    # View musi wiedziec na jakim coursie operuje.
    # Request przychodzi raz z parametrami.
    # my zapisuje course ktor obecnie widok przetwarza/wyswietla
    # Po co ? Po te musimy wiedziec jakie module wyswietlic
    # dispatch przekazuje dalej do get() i post()
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super(CourseModuleUpdateView,self).dispatch(request, pk)

    # To co chcemy przekaza templatowi
    # self.course memy bo przechwicilismy go w dispatch
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    # Get model for for view
    def get_model(self, model_name):
        if model_name in ['text','video','image','file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None


    # Build for for the view based on model.
    # Common fields are not required.
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args,**kwargs)


    def dispatch(self, request, module_id, model_name, id=None):
        print(module_id)
        print(model_name)
        self.module = get_object_or_404(Module,
                                        id=module_id)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super(ContentCreateUpdateView,self).dispatch(request,module_id,model_name, id)


    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form' : form,
                                        'object': self.obj})


    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module,item=obj)
            return redirect('module_content_list', self.module.id)

        return self.render_to_response({'form': form,
                                    'object': self.obj})


# Delete content from module
# HTTP 405 received
class ContentDeleteView(View):

    def post(self, request, id):
        # TODO - nie dziala. Wczesniej 405
        if request.session.get('delete_allowed') is None:
            return HttpResponseNotFound("Cannot delete view directly")
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        del request.session['delete_allowed']
        return redirect('module_content_list', module.id)


# Load all content for modules
class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        # set delete_allowed variable in session
        request.session['delete_allowed'] = 'true'
        return self.render_to_response({'module': module})


# View to display all courses or filtered (based on subject)
class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(
            total_courses=Count('courses'))
        courses = Course.objects.annotate(
            total_modules=Count('modules'))

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})



# View to display single course
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView,
                        self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})
        return context

