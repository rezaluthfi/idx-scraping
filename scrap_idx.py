import os
import time
import base64
import undetected_chromedriver as uc

def download_idx_financial_report(tickers, year, period="Audit", output_dir="downloads"):
    period_clean = str(period).lower().strip()
    period_map = {
        "audit": "audit",
        "tahunan": "audit",
        "annual": "audit",
        "tw1": "tw1",
        "q1": "tw1",
        "quarter 1": "tw1",
        "tw2": "tw2",
        "q2": "tw2",
        "quarter 2": "tw2",
        "tw3": "tw3",
        "q3": "tw3",
        "quarter 3": "tw3"
    }
    api_period = period_map.get(period_clean, "audit")
    
    print("=" * 60)
    print("      IDX FINANCIAL REPORT SCRAPER      ")
    print("=" * 60)
    print(f"Target Emiten : {', '.join(tickers)}")
    print(f"Tahun         : {year}")
    print(f"Periode       : {period} (API: {api_period})")
    print(f"Folder Output : {os.path.abspath(output_dir)}")
    print("=" * 60)
    
    print("\n[1/3] Menyiapkan browser...")
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    
    try:
        print("[2/3] Membuka portal IDX...")
        driver.get("https://www.idx.co.id/id/perusahaan-tercatat/laporan-keuangan-dan-tahunan")
        
        for _ in range(15):
            time.sleep(1)
            title = driver.title
            if title and "Attention Required" not in title and "Just a moment" not in title:
                print(f"[Sukses] Terhubung ke IDX: '{title}'\n")
                break
        else:
            print("[Peringatan] Verifikasi Cloudflare mungkin memerlukan interaksi manual.")

        fetch_api_js = """
        const [url, callback] = [arguments[0], arguments[arguments.length - 1]];
        fetch(url, {
            headers: {
                'Accept': 'application/json, text/plain, */*'
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('HTTP Status: ' + response.status);
            return response.json();
        })
        .then(data => callback({success: true, data: data}))
        .catch(err => callback({success: false, error: err.toString()}));
        """

        download_file_js = """
        const [url, callback] = [arguments[0], arguments[arguments.length - 1]];
        fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('HTTP Status: ' + response.status);
            return response.blob();
        })
        .then(blob => {
            const reader = new FileReader();
            reader.onloadend = () => callback({success: true, data: reader.result});
            reader.onerror = () => callback({success: false, error: 'File read error'});
            reader.readAsDataURL(blob);
        })
        .catch(err => callback({success: false, error: err.toString()}));
        """

        print("[3/3] Memulai penarikan data dan pengunduhan berkas...\n")
        
        for ticker in tickers:
            ticker = ticker.upper().strip()
            print(f"------------------------------------------------------------")
            print(f"Mencari laporan untuk: {ticker} ({year} - {api_period})")
            print(f"------------------------------------------------------------")
            
            api_url = (
                f"https://www.idx.co.id/primary/ListedCompany/GetFinancialReport"
                f"?kodeEmiten={ticker}&year={year}&periode={api_period}"
                f"&indexFrom=0&pageSize=100&reportType=rdf"
            )
            
            res = driver.execute_async_script(fetch_api_js, api_url)
            
            if not res or not res.get("success"):
                print(f"[Gagal] Kendala saat mengambil data emiten {ticker}: {res.get('error') if res else 'Unknown error'}")
                continue
                
            results = res.get("data", {}).get("Results", [])
            if not results:
                print(f"[Info] Tidak ada data laporan keuangan ditemukan untuk {ticker} pada periode tersebut.")
                continue
                
            target_folder = os.path.join(output_dir, f"{ticker}_{year}_{api_period}")
            os.makedirs(target_folder, exist_ok=True)
            
            download_count = 0
            for item in results:
                attachments = item.get("Attachments", [])
                for att in attachments:
                    file_name = att.get("File_Name")
                    file_path = att.get("File_Path")
                    
                    if not file_name or not file_path:
                        continue
                        
                    file_url = f"https://www.idx.co.id{file_path}"
                    dest_file = os.path.join(target_folder, file_name)
                    
                    if os.path.exists(dest_file) and os.path.getsize(dest_file) > 0:
                        size_mb = os.path.getsize(dest_file) / (1024 * 1024)
                        print(f"  [Sudah Ada] {file_name} ({size_mb:.2f} MB)")
                        download_count += 1
                        continue
                        
                    print(f"  [Mengunduh] {file_name} ...", end=" ", flush=True)
                    dl_res = driver.execute_async_script(download_file_js, file_url)
                    
                    if dl_res and dl_res.get("success"):
                        data_url = dl_res["data"]
                        header, encoded = data_url.split(",", 1)
                        file_bytes = base64.b64decode(encoded)
                        
                        with open(dest_file, "wb") as f:
                            f.write(file_bytes)
                            
                        size_mb = len(file_bytes) / (1024 * 1024)
                        print(f"SUKSES ({size_mb:.2f} MB)")
                        download_count += 1
                    else:
                        err_msg = dl_res.get("error") if dl_res else "Timeout/Error"
                        print(f"GAGAL ({err_msg})")
                        
                    time.sleep(0.3)
                    
            print(f"-> Selesai untuk {ticker}. Berhasil mengunduh/memverifikasi {download_count} berkas.\n")
            time.sleep(1)

        print("=" * 60)
        print("SEMUA PROSES SELESAI!")
        print(f"Direktori penyimpanan: {os.path.abspath(output_dir)}")
        print("=" * 60)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    kode_saham = ["BBCA", "TLKM"]
    tahun = 2023
    periode = "Audit"
    
    download_idx_financial_report(kode_saham, tahun, periode)