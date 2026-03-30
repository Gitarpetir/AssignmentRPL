import httpx
from mcp.server.fastmcp import FastMCP

# 1. Mendirikan bangunan jembatan
mcp = FastMCP("Server Cuaca BMKG")

# 2. Alat Pertama: Mengecek cuaca yang paling dekat dengan waktu saat ini
@mcp.tool()
async def cek_cuaca_terkini_bmkg(kode_wilayah: str) -> str:
    """Mengecek cuaca terkini di Indonesia berdasarkan Kode Wilayah Desa/Kelurahan (adm4). Contoh kode: 31.71.03.1001"""
    
    url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode_wilayah}"
    
    try:
        async with httpx.AsyncClient() as client:
            respons = await client.get(url)
            
            # Sistem Pengereman: Jika kita terlalu sering memanggil (Batas 60x/menit)
            if respons.status_code == 429:
                return "Maaf, kita bertanya terlalu cepat ke BMKG. Tunggu sekitar satu menit lalu coba lagi."
            elif respons.status_code != 200:
                return "Maaf, satelit BMKG sedang sibuk atau kode wilayah tidak ditemukan."
            
            data = respons.json()
            
            # BMKG menyimpan data cuacanya di dalam struktur JSON yang bertingkat.
            # Kita mengambil data pertama dari daftar (index 0) yang merupakan waktu terdekat.
            # (Menggunakan try-except khusus di sini agar tahan banting jika struktur data BMKG berubah)
            try:
                # Menelusuri laci JSON BMKG
                data_lokasi = data["data"][0]
                nama_lokasi = data_lokasi["lokasi"]["desa"]
                cuaca_terdekat = data_lokasi["cuaca"][0][0] # Mengambil hari ini, jam terdekat
                
                waktu = cuaca_terdekat["local_datetime"]
                suhu = cuaca_terdekat["t"]
                kondisi = cuaca_terdekat["weather_desc"]
                kelembapan = cuaca_terdekat["hu"]
                angin = cuaca_terdekat["ws"]
                
                return f"Laporan BMKG untuk Kelurahan {nama_lokasi} pada {waktu}:\nCuaca: {kondisi}\nSuhu: {suhu}°C\nKelembapan: {kelembapan}%\nKecepatan Angin: {angin} km/jam."
            
            except (KeyError, IndexError):
                return "Berhasil menghubungi BMKG, namun gagal membaca format laporannya."
                
    except Exception:
        return "Gagal menyambung ke internet. Periksa koneksimu."


# 3. Alat Kedua: Melihat rangkuman prakiraan untuk beberapa jam ke depan
@mcp.tool()
async def cek_prakiraan_harian_bmkg(kode_wilayah: str) -> str:
    """Melihat prakiraan cuaca BMKG per 3 jam untuk hari ini berdasarkan Kode Wilayah (adm4)."""
    
    url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode_wilayah}"
    
    try:
        async with httpx.AsyncClient() as client:
            respons = await client.get(url)
            
            if respons.status_code == 429:
                return "Sistem pengereman aktif: Tunggu satu menit sebelum meminta data lagi."
            elif respons.status_code != 200:
                return "Gagal mengambil data dari BMKG."
            
            data = respons.json()
            
            try:
                nama_lokasi = data["data"][0]["lokasi"]["desa"]
                # Mengambil daftar cuaca untuk hari pertama saja
                daftar_cuaca_hari_ini = data["data"][0]["cuaca"][0] 
                
                hasil = f"Prakiraan Cuaca Hari Ini di {nama_lokasi}:\n"
                
                # Kita buat perulangan (loop) untuk merangkum semua jadwal per 3 jam
                for jadwal in daftar_cuaca_hari_ini:
                    waktu = jadwal["local_datetime"].split(" ")[1] # Hanya mengambil jamnya saja
                    kondisi = jadwal["weather_desc"]
                    suhu = jadwal["t"]
                    hasil += f"- Jam {waktu}: {kondisi} ({suhu}°C)\n"
                
                return hasil
                
            except (KeyError, IndexError):
                return "Format data cuaca harian tidak sesuai."
                
    except Exception:
        return "Gagal menyambung ke internet."

if __name__ == "__main__":
    # 4. Menyalakan jembatan
    mcp.run()