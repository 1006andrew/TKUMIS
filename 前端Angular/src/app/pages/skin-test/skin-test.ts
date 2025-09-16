import { Component, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-skin-test',
  standalone: true,
  templateUrl: './skin-test.html',
  imports: [CommonModule, FormsModule],
  styleUrls: ['./skin-test.css']
})

export class SkinTestComponent {
  selectedFile: File | null = null;
  previewUrl: string | ArrayBuffer | null = null;
  result: any = null;
  loading = false;

  // ✅ 使用者清單
  users: any[] = [];
  selectedUserId: string | null = null;

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      this.selectedFile = input.files[0];
      const reader = new FileReader();
      reader.onload = () => this.previewUrl = reader.result;
      reader.readAsDataURL(this.selectedFile);
      this.result = null;
    }
  }

  onSubmit(): void {
    if (!this.selectedFile) {
      alert("請先選擇圖片！");
      return;
    }

    this.result = null;
    this.loading = true;

    const formData = new FormData();
    formData.append('file', this.selectedFile, this.selectedFile.name);

    this.http.post('http://localhost:8000/skintest/analyze', formData, {
      headers: { 'Cache-Control': 'no-cache' }
    })
    .subscribe({
      next: (res: any) => {
        console.log("🔥 原始後端回應:", res);

        this.result = {
          oil_label: res.oil_label,
          oil_prob: res.oil_prob,
          sensi_label: res.sensi_label,
          sensi_prob: res.sensi_prob
        };

        this.loading = false;
        this.cdr.detectChanges();

        // ✅ 分析完才載入使用者清單
        this.fetchUsers();
      },
      error: err => {
        console.error("❌ 上傳失敗:", err);
        this.loading = false;
      }
    });
  }

  // ✅ 撈取所有使用者
  fetchUsers() {
    this.http.get<any[]>('http://localhost:8000/admin/clients/json')
      .subscribe({
        next: (res) => {
          this.users = res;
        },
        error: (err) => {
          console.error("❌ 無法取得使用者清單:", err);
        }
      });
  }

  // ✅ 寫入膚質結果
  saveResult() {
    if (!this.selectedUserId || !this.result) {
      alert("⚠️ 請先選擇使用者並完成分析！");
      return;
    }

    const payload = {
      client_id: this.selectedUserId,
      ...this.result
    };

    this.http.post('http://localhost:8000/skintest/save_result', payload)
      .subscribe({
        next: () => alert(`✅ 已將膚質結果寫入使用者 ${this.selectedUserId}`),
        error: (err) => console.error("❌ 寫入失敗:", err)
      });
  }
}
