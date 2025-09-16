import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Firestore, collection, collectionData, addDoc, deleteDoc, doc } from '@angular/fire/firestore';
import { Observable } from 'rxjs';
import { ClientsListComponent } from "./clients-list/clients-list";
import { ProductsListComponent } from "./products-list/products-list";
import { RecordsListComponent } from "./records-list/records-list";
import { DetailComponent } from "./detail/detail";
import { SkinTestComponent } from "../skin-test/skin-test";
import { BookingsListComponent } from "./bookings-list/bookings-list";

interface UserData {
  id?: string;
  name: string;
  email: string;
}

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, FormsModule, ClientsListComponent, ProductsListComponent, RecordsListComponent, DetailComponent, SkinTestComponent, BookingsListComponent],
  templateUrl: './admin.html',
  styleUrls: ['./admin.css']
})
export class AdminComponent implements OnInit {
  users$!: Observable<UserData[]>;
  newUser: UserData = { name: '', email: '' };

  page: string = 'dashboard';
  detailItem: any = null;

  constructor(private firestore: Firestore) {}

  ngOnInit() {
    const userCollection = collection(this.firestore, 'users');
    this.users$ = collectionData(userCollection, { idField: 'id' }) as Observable<UserData[]>;

    // ✅ 讀取 localStorage 的預設頁面
    const defaultPage = localStorage.getItem('adminDefaultPage');
    if (defaultPage) {
      this.page = defaultPage;
      localStorage.removeItem('adminDefaultPage'); // 用完就刪掉
    }
  }

  async addUser() {
    if (!this.newUser.name || !this.newUser.email) return;
    const userCollection = collection(this.firestore, 'users');
    await addDoc(userCollection, this.newUser);
    this.newUser = { name: '', email: '' };
  }

  async deleteUser(userId: string) {
    const userDoc = doc(this.firestore, `users/${userId}`);
    await deleteDoc(userDoc);
  }

  navigateTo(page: string) {
    this.page = page;
  }

  openDetail(item: any) {
    this.detailItem = item;
    this.page = 'detail';
  }
}
