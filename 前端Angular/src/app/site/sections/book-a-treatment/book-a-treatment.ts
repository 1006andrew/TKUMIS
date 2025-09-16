import { Component, effect, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Profile, ProfileService } from '../../../service/profile';
import { AuthService } from '../../../service/auth';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-book-a-treatment',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './book-a-treatment.html',
  styleUrls: ['./book-a-treatment.css'],
})

export class BookATreatmentComponent {
  private api = inject(ProfileService);
  private auth = inject(AuthService);
  private http = inject(HttpClient);

  loading = signal(true);
  profile = signal<Profile | null>(null);
  error = signal<string | null>(null);

  // ✅ 療程選擇
  // ✅ 療程清單
  treatments = [
    '胜肽水光護理課程',
    '4D膠原極致澎亮臉部護理',
    '7D天使光護理課程',
    '美AI科技智能溫塑按摩課程',
  ];
  selectedTreatment: string | null = null;

  // ✅ 日期 / 時間
  selectedDate: string | null = null;
  selectedTime: string | null = null;

  constructor() {
    effect(() => {
      const user = this.auth.user();
      if (user && user.uid) {
        this.fetchData(user.uid);
      }
    });
  }

  private fetchData(userId: string) {
    this.loading.set(true);
    this.error.set(null);

    this.api.getMyProfileById(userId).subscribe({
      next: (p) => {
        this.profile.set(p);
        this.loading.set(false);
      },
      error: (e) => {
        this.error.set(e?.message ?? '載入使用者資料失敗');
        this.loading.set(false);
      },
    });
  }

  // ✅ 送出預約
  submitBooking() {
    if (!this.profile() || !this.selectedTreatment || !this.selectedDate || !this.selectedTime) {
      this.error.set('請填寫完整預約資訊');
      return;
    }

    const booking = {
      userId: this.profile()!.id,
      treatment: this.selectedTreatment,
      date: this.selectedDate,
      time: this.selectedTime,
      createdAt: new Date().toISOString(),
    };

    // 呼叫後端 API，把預約寫進 Firestore
    this.http.post('http://localhost:8000/api/bookings', booking).subscribe({
      next: () => {
        alert('預約成功！');
        this.selectedTreatment = null;
        this.selectedDate = null;
        this.selectedTime = null;
      },
      error: (e) => {
        console.error(e);
        this.error.set('預約失敗，請稍後再試');
      },
    });
  }
}
