import { Routes } from '@angular/router';
import { HomeComponent } from './home/home';
import { LoginComponent } from './login/login';

import { SkinTestComponent } from './pages/skin-test/skin-test';
import { BrandComponent } from './site/sections/brand/brand';
import { ProductComponent } from './site/sections/product/product';
import { ContactComponent } from './site/sections/contact/contact';
import { TherapyComponent } from './site/sections/therapy/therapy';
import { AdminComponent } from './pages/admin/admin';
import { inject } from '@angular/core';
import { AuthService } from './service/auth';
import { BookATreatmentComponent } from './site/sections/book-a-treatment/book-a-treatment';
import { PersonalPageComponent } from './pages/personal-page/personal-page';

export const routes: Routes = [
  // 首頁進來就 redirect 到 /book-a-treatment
  { path: '', redirectTo: 'brand', pathMatch: 'full' },

  { path: 'home', component: HomeComponent },

  { path: 'book-a-treatment', component: BookATreatmentComponent },
  { path: 'skin-test', component: SkinTestComponent },

  // navbar 四個頁面
  { path: 'login', component: LoginComponent },
  { path: 'personal-page', component: PersonalPageComponent },
  { path: 'brand', component: BrandComponent },
  { path: 'product', component: ProductComponent },
  { path: 'therapy', component: TherapyComponent },
  { path: 'contact', component: ContactComponent },

  //
  {
    path: 'admin',
    component: AdminComponent,
    canActivate: [
      async () => {
        const auth = inject(AuthService);
        if (await auth.isAdmin()) {
          return true;
        } else {
          alert('你沒有權限進入管理者頁面');
          return false;
        }
      },
    ],
  },

  {
    path: 'chatbot',
    loadComponent: () => import('./pages/chatbot/chatbot').then((m) => m.ChatbotComponent),
  },

  // 萬一路由不存在，就回首頁
  { path: '**', redirectTo: 'login' },
];
