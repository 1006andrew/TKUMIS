import { Injectable } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth';

@Injectable({
  providedIn: 'root'
})

export class AdminGuard {
  constructor(private auth: AuthService, private router: Router) {}

  async canActivate(): Promise<boolean> {
    const isAdmin = await this.auth.isAdmin();
    if (isAdmin) {
      return true;
    } else {
      alert('你沒有權限進入管理者頁面');
      this.router.navigate(['/login']); // ✅ 轉回登入頁
      return false;
    }
  }
}
