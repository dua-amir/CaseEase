from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Case
from .forms import CaseForm, AssignHandlerForm
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import CaseHistory

# Create your views here.


class RegisterCaseView(LoginRequiredMixin, CreateView):
    model = Case
    form_class = CaseForm
    template_name = 'cases/register_case.html'
    success_url = reverse_lazy('user_dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        # Log registration
        CaseHistory.objects.create(
            case=self.object,
            action="Case Registered",
            performed_by=self.request.user
        )

        return response




class CaseDetailView(DetailView):
    model = Case
    template_name = 'cases/case_detail.html'
    context_object_name = 'case'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history'] = self.object.history.order_by('-timestamp')
        return context
    



User = get_user_model()

class AssignHandlerView(View):
    def get(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        form = AssignHandlerForm(instance=case)
        form.fields['assigned_to'].queryset = User.objects.filter(groups__name__iexact='handler')
        return render(request, 'cases/assign_handler.html', {'form': form, 'case': case})

    def post(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        form = AssignHandlerForm(request.POST, instance=case)
        form.fields['assigned_to'].queryset = User.objects.filter(groups__name__iexact='handler')

        if form.is_valid():
            case = form.save(commit=False)
            case.status = 'Assigned'
            case.save()

            # Log assignment to history
            CaseHistory.objects.create(
                case=case,
                action=f"Assigned to {case.assigned_to.username}",
                performed_by=request.user
            )

            return redirect('approved_cases')

        # Re-render form if invalid
        return render(request, 'cases/assign_handler.html', {'form': form, 'case': case})
