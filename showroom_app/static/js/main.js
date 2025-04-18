function showLogoutConfirmation() {
    Swal.fire({
        title: 'Konfirmasi Logout',
        text: "Anda yakin ingin keluar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Ya, Logout',
        cancelButtonText: 'Batal'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('logout-form').submit();
        }
    })
}

function formatRupiah(angka) {
    let number_string = angka.replace(/[^,\d]/g, ''),
        sisa = number_string.length % 3,
        rupiah = number_string.substr(0, sisa),
        ribuan = number_string.substr(sisa).match(/\d{3}/gi);

    if (ribuan) {
        let separator = sisa ? '.' : '';
        rupiah += separator + ribuan.join('.');
    }

    return rupiah;
}

document.addEventListener('DOMContentLoaded', function () {
    const rupiahInputs = document.querySelectorAll('.rupiah');

    rupiahInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            // Save cursor position
            const value = this.value.replace(/\D/g, '');
            const caret = this.selectionStart;
            const formatted = formatRupiah(value);
            this.value = formatted;

            // Optional: try to restore caret to right side (not perfect)
            this.setSelectionRange(this.value.length, this.value.length);
        });

        // Before form submits, strip formatting
        const form = input.closest('form');
        if (form) {
            form.addEventListener('submit', function () {
                input.value = input.value.replace(/\D/g, '');
            });
        }
    });
});