from django.db import models

class Mobil(models.Model):
    id = models.AutoField(primary_key=True)
    merk = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    tahun = models.PositiveIntegerField()
    harga_dasar = models.DecimalField(max_digits=15, decimal_places=2)
    pinjaman_bank = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    suku_bunga = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.merk} {self.model} ({self.tahun})"
   
    def get_bunga_bulanan(self):
        if self.pinjaman_bank and self.suku_bunga is not None:
            if float(self.suku_bunga) == 0:
                return 0
            else:
                return (float(self.suku_bunga) / 100) / 12
        return None

    def cicilan(self, bulan):
        bunga_bulanan = self.get_bunga_bulanan()
        if self.pinjaman_bank and bunga_bulanan is not None:
            if float(self.suku_bunga) == 0:
                return round(float(self.pinjaman_bank) / bulan, 2)
            else:
                pokok = float(self.pinjaman_bank)
                cicilan = (pokok * bunga_bulanan) / (1 - (1 + bunga_bulanan) ** -bulan)
                return round(cicilan, 2)
        return None

    def cicilan_satu(self):
        return self.cicilan(12)

    def cicilan_tiga(self):
        return self.cicilan(36)

    def cicilan_lima(self):
        return self.cicilan(60)

    def calculate_hpp(self):
        total_service = sum([service.biaya for service in self.services.all()])
        if self.pinjaman_bank and self.suku_bunga is not None:
            try:
                pinjaman = float(self.pinjaman_bank)
                suku_bunga = float(self.suku_bunga) / 100
                total_interest = pinjaman + suku_bunga
                return round(
                    float(self.harga_dasar) /
                    total_interest +
                    float(total_service),
                    2
                )
            except Exception as e:
                print(f"Error calculating HPP: {e}")
                return None
        return None

class Service(models.Model):
    mobil = models.ForeignKey(Mobil, on_delete=models.CASCADE, related_name='services')
    tanggal_service = models.DateField()
    deskripsi = models.TextField()
    biaya = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Service {self.mobil} pada {self.tanggal_service}"
