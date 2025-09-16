import { Component, computed, effect, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Profile, ProfileService } from '../../service/profile';
import { AuthService } from '../../service/auth';

@Component({
  selector: 'app-personal-page',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './personal-page.html',
  styleUrl: './personal-page.css'
})
export class PersonalPageComponent {
  private api = inject(ProfileService);
  private auth = inject(AuthService);

  loading = signal(true);
  profile = signal<Profile | null>(null);
  error = signal<string | null>(null);

  constructor() {
    // ✅ 偵測使用者登入狀態，自動抓資料
    effect(() => {
      const user = this.auth.user();
      if (user && user.uid) {
        this.fetchData(user.uid);
      }
    });
  }

  // ✅ 頭像字母
  get avatarInitial() {
    const n = this.profile()?.displayName ?? '';
    return n ? n[0].toUpperCase() : '?';
  }

  // ✅ 統計資訊
  stats = computed(() => {
    const p = this.profile();
    return [
      { label: '點數', value: p?.points ?? 0 },
      { label: '預約數', value: p?.bookingsCount ?? 0 },
      { label: '膚質', value: p?.skinType ?? '—' }
    ];
  });

  // ✅ 使用 userId 直接呼叫 API
  private fetchData(userId: string) {
    this.loading.set(true);
    this.error.set(null);

    this.api.getMyProfileById(userId).subscribe({
      next: (p) => {
        this.profile.set(p);
        this.loading.set(false);
      },
      error: (e) => {
        this.error.set(e?.message ?? '載入個人資料失敗');
        this.loading.set(false);
      }
    });
  }
}
