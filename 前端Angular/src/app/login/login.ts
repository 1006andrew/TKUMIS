import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../service/auth';   // ✅ 引入 AuthService

// Firebase
import { Auth, signInWithPopup, GoogleAuthProvider } from '@angular/fire/auth';
import { doc, Firestore, setDoc } from '@angular/fire/firestore';

interface AuthOut {
  ok: boolean;
  message: string;
  redirect?: string | null;
  user?: any;
}

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css'],
})
export class LoginComponent {
  mode: 'login' | 'register' = 'login';
  email = '';
  password = '';
  name = '';
  message: string | null = null;
  loading = false;

  private apiBase = 'http://localhost:8000/api/users';
  private auth = inject(Auth);
  private firestore = inject(Firestore); // 注入Firestore

  constructor(
    private http: HttpClient,
    private router: Router,
    private authService: AuthService   // ✅ 注入共用 AuthService
  ) {}

  toggleForm(mode: 'login' | 'register') {
    this.mode = mode;
    this.message = null;
  }

  handleLogin() {
    this.loading = true;
    this.http.post<AuthOut>(`${this.apiBase}/login`, {
      email: this.email,
      password: this.password,
    }).subscribe({
      next: (res) => {
        if (res.ok) {
          this.message = res.message || '登入成功';
          // ✅ 保存使用者狀態
          if (res.user) this.authService.setUser(res.user);

          this.router.navigateByUrl('/');
        } else {
          this.message = res.message || '登入失敗';
        }
        this.loading = false;
      },
      error: () => {
        this.message = '系統錯誤';
        this.loading = false;
      },
    });
  }

  handleRegister() {
    this.loading = true;
    this.http.post<AuthOut>(`${this.apiBase}/register`, {
      name: this.name,
      email: this.email,
      password: this.password,
    }).subscribe({
      next: (res) => {
        if (res.ok) {
          this.message = res.message || '註冊成功';
          this.toggleForm('login');
        } else {
          this.message = res.message || '註冊失敗';
        }
        this.loading = false;
      },
      error: () => {
        this.message = '系統錯誤';
        this.loading = false;
      },
    });
  }

  async handleGoogleLogin() {
    this.loading = true;
    try {
      const provider = new GoogleAuthProvider();
      const result = await signInWithPopup(this.auth, provider);

      const userInfo = {
        uid: result.user.uid,
        name: result.user.displayName,
        email: result.user.email,
        photoURL: result.user.photoURL,
        createdAt: new Date()
      };
      this.authService.setUser(userInfo);  // ✅ 保存登入者
      console.log("[DEBUG] Google 使用者資訊 :",userInfo)

      //
      const userRef = doc(this.firestore, `clients/${userInfo.uid}`);
      try {
        await setDoc(userRef, userInfo, {merge:true});
      } catch (firestoreErr) {
        console.error("[DEBUG] Firestore 寫入失敗 :", firestoreErr)
        this.message = "寫入失敗";
        this.loading = false; // ??
        return
      }

      console.log("[DEBUG] 成功寫入Firestore -> clients/", userInfo.uid)


      const idToken = await result.user.getIdToken();
      this.http.post<AuthOut>('http://localhost:8000/auth/google/login', { id_token: idToken })
        .subscribe({
          next: (res) => {
            this.message = res.message || 'Google 登入成功';
            this.router.navigateByUrl('/');
            this.loading = false;
          },
          error: () => {
            this.message = 'Google 登入錯誤';
            this.loading = false;
          },
        });
    } catch (err) {
      // console.error(err);
      // this.message = 'Google 登入失敗';
      // this.loading = false;
    }
  }
}
