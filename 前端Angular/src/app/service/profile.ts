import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

/**
 * 使用者 Profile 型別
 */
export type Profile = {
  id: string;
  displayName: string;
  email?: string;
  phone?: string;
  avatarUrl?: string;
  points?: number;
  bookingsCount?: number;
  skinType?: string;
  lastVisitAt?: string; // ISO string
};

@Injectable({ providedIn: 'root' })
export class ProfileService {
  private http = inject(HttpClient);

  // ✅ 後端 personal_page API base
  private readonly baseUrl = 'http://localhost:8000/api/personal_page';

  /**
   * ✅ 取得目前登入使用者的個人資料
   * @param params.user_id Firestore 使用者 id
   */
  getMyProfile(params?: { user_id?: string }): Observable<Profile> {
    const query = params?.user_id ? `?user_id=${encodeURIComponent(params.user_id)}` : '';
    return this.http.get<Profile>(`${this.baseUrl}/me${query}`);
  }

  /**
   * ✅ 依 userId 直接取個人資料（語法糖）
   */
  getMyProfileById(userId: string): Observable<Profile> {
    return this.http.get<Profile>(`${this.baseUrl}/me?user_id=${encodeURIComponent(userId)}`);
  }
}
