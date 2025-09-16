// src/app/service/auth.ts
import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';

export interface AuthOut {
  ok: boolean;
  message: string;
  redirect?: string | null;
  user?: any;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private userBaseUrl = 'http://localhost:8000/api/users'; // ⚠️ 記得跟後端 router 對應
  private googleBaseUrl = 'http://localhost:8000/auth/google';

  // ✅ 使用 Angular signal 保存目前登入者
  user = signal<any>(null);

  // ✅ 只有這個 email 是管理者
  private adminEmail = 'zc754615@gmail.com';

  constructor(private http: HttpClient, private router: Router) {}

  // email / password 登入
  login(email: string, password: string): Observable<AuthOut> {
    return this.http.post<AuthOut>(`${this.userBaseUrl}/login`, { email, password });
  }

  // firebase id_token 登入
  loginWithToken(idToken: string): Observable<AuthOut> {
    return this.http.post<AuthOut>(`${this.googleBaseUrl}/login`, { id_token: idToken });
  }

  // ✅ 設定/清除使用者
  setUser(u: any) {
    this.user.set(u);
  }

  clearUser() {
    this.user.set(null);
    this.router.navigateByUrl('/login');
  }

  // ✅ 假設登入成功時呼叫，存使用者資訊（包含 uid）
  loginSuccess(userData: any) {
    this.user.set(userData);  // userData 需包含至少 { uid, email, displayName }
  }

  /**
   * ✅ 判斷是否為管理者
   */
  isAdmin(): boolean {
    const currentUser = this.user();
    if (!currentUser) return false;

    const email = currentUser.email || '';
    return email === this.adminEmail;
  }

  /**
   * ✅ 判斷是否為 Firestore 使用者
   * 會自動從 currentUser 讀取 email
   */
  isUser(): Observable<{ exists: boolean }> {
    const currentUser = this.user();
    if (!currentUser || !currentUser.email) {
      throw new Error('尚未登入，無法檢查使用者');
    }

    const email = currentUser.email;
    return this.http.get<{ exists: boolean }>(
      `${this.userBaseUrl}/check?email=${encodeURIComponent(email)}`
    );
  }
}
