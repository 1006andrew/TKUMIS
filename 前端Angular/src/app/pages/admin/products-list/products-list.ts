// src/app/pages/admin/products-list/products-list.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  Firestore,
  collection,
  collectionData,
  addDoc,
  deleteDoc,
  doc,
  updateDoc,
  serverTimestamp
} from '@angular/fire/firestore';
import { Observable } from 'rxjs';

interface Product {
  id?: string;
  order_no: string;
  price_max: number;
  price_min: number;
  product_name: string;
  updated_at: any;
}

@Component({
  selector: 'app-products-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './products-list.html',
  styleUrls: ['./products-list.css'],
})
export class ProductsListComponent implements OnInit {
  products$!: Observable<Product[]>;
  newProduct: Product = {
    product_name: '',
    order_no: '',
    price_max: 0,
    price_min: 0,
    updated_at: null,
  };

  editMode: string | null = null; // 目前正在編輯的產品 ID
  editProduct: Product | null = null;

  constructor(private firestore: Firestore) {}

  ngOnInit() {
    const ref = collection(this.firestore, 'products');
    this.products$ = collectionData(ref, { idField: 'id' }) as Observable<
      Product[]
    >;

    this.products$.subscribe((data) => {
      console.log('[DEBUG] Firestore products =>', data);
    });
  }

  /** 新增產品 */
  async addProduct() {
    if (!this.newProduct.product_name || !this.newProduct.order_no) return;

    const ref = collection(this.firestore, 'products');
    await addDoc(ref, {
      ...this.newProduct,
      updated_at: serverTimestamp(),
    });

    // reset form
    this.newProduct = {
      product_name: '',
      order_no: '',
      price_max: 0,
      price_min: 0,
      updated_at: null,
    };
  }

  /** 刪除產品 */
  async deleteProduct(productId: string) {
    const productDoc = doc(this.firestore, `products/${productId}`);
    await deleteDoc(productDoc);
  }

  /** 進入編輯模式 */
  startEdit(product: Product) {
    this.editMode = product.id || null;
    this.editProduct = { ...product }; // copy
  }

  /** 更新產品 */
  async updateProduct() {
    if (!this.editProduct?.id) return;
    const productDoc = doc(this.firestore, `products/${this.editProduct.id}`);
    await updateDoc(productDoc, {
      ...this.editProduct,
      updated_at: serverTimestamp(),
    });

    this.editMode = null;
    this.editProduct = null;
  }

  /** 取消編輯 */
  cancelEdit() {
    this.editMode = null;
    this.editProduct = null;
  }
}
