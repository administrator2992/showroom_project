from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, views as auth_views, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Mobil, Service
from django.db.models import Q
from .forms import MobilForm, ServiceForm, UserRegistrationForm

class MessageLogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Anda telah berhasil logout!")
        return super().dispatch(request, *args, **kwargs)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('mobil_list')
        else:
            messages.error(request, "Username atau password salah!")
            return redirect('login')  # Redirect back to login page
    
    return render(request, 'login.html')

def mobil_list(request):
    search_query = request.GET.get('q', '')
    
    mobils = Mobil.objects.all().order_by('-id')
    
    if search_query:
        # Try to convert to integer for tahun search
        try:
            tahun_query = int(search_query)
        except ValueError:
            tahun_query = None
            
        mobils = mobils.filter(
            Q(merk__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(tahun__exact=tahun_query)
        ).distinct()

    return render(request, 'mobil_list.html', {'mobils': mobils})

def mobil_detail(request, pk):
    """Show detailed car information with service history and calculations"""
    mobil = get_object_or_404(Mobil, pk=pk)
    services = mobil.services.all()

    total_service = sum(service.biaya for service in services)
    
    # Calculate monthly installment
    cicilan_satu = mobil.cicilan_satu()
    cicilan_tiga = mobil.cicilan_tiga()
    cicilan_lima = mobil.cicilan_lima()
    
    return render(request, 'mobil_detail.html', {
        'mobil': mobil,
        'services': services,
        'cicilan_satu': cicilan_satu,
        'cicilan_tiga': cicilan_tiga,
        'cicilan_lima': cicilan_lima,
        'hpp': mobil.calculate_hpp(),
        'total_service': total_service
    })

@login_required
def mobil_create(request):
    """Create new car entry (protected view)"""
    if request.method == 'POST':
        form = MobilForm(request.POST)
        if form.is_valid():
            new_mobil = form.save()
            messages.success(request, 'Mobil berhasil ditambahkan!')
            return redirect('mobil_detail', pk=new_mobil.pk)
    else:
        form = MobilForm()
    return render(request, 'mobil_form.html', {'form': form})

@login_required
def mobil_update(request, pk):
    """Update existing car entry (protected view)"""
    mobil = get_object_or_404(Mobil, pk=pk)
    if request.method == 'POST':
        form = MobilForm(request.POST, instance=mobil)
        if form.is_valid():
            updated_mobil = form.save()
            messages.success(request, 'Data mobil berhasil diperbarui!')
            return redirect('mobil_detail', pk=updated_mobil.pk)
    else:
        form = MobilForm(instance=mobil)
    return render(request, 'mobil_form.html', {'form': form})

@login_required
def mobil_delete(request, pk):
    """Delete car entry (protected view)"""
    mobil = get_object_or_404(Mobil, pk=pk)
    if request.method == 'POST':
        mobil.delete()
        messages.success(request, 'Mobil berhasil dihapus!')
        return redirect('mobil_list')
    return render(request, 'mobil_confirm_delete.html', {'mobil': mobil})

@login_required
def service_create(request, mobil_pk):
    """Add service record to a car (protected view)"""
    mobil = get_object_or_404(Mobil, pk=mobil_pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.mobil = mobil
            service.save()
            messages.success(request, 'Data service berhasil ditambahkan!')
            return redirect('mobil_detail', pk=mobil.pk)
    else:
        form = ServiceForm()
    return render(request, 'service_form.html', {'form': form, 'mobil': mobil})

@login_required
def change_password(request):
    """Change user password (protected view)"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password berhasil diubah!')
            return redirect('mobil_list')
        else:
            pass
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})