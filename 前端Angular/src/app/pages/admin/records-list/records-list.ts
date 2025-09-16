// src/app/pages/admin/records-list/records-list.ts
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

interface PurchaseRecord {
  id?: string;
  client_id: number;
  product_id: number;
  quantity: number;
  amount: number;
  order_date: any;
  created_at: any;
  updated_at: any;
}

@Component({
  selector: 'app-records-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './records-list.html',
  styleUrls: ['./records-list.css']
})
export class RecordsListComponent implements OnInit {
  records$!: Observable<PurchaseRecord[]>;

  newRecord: PurchaseRecord = {
    client_id: 0,
    product_id: 0,
    quantity: 1,
    amount: 0,
    order_date: null,
    created_at: null,
    updated_at: null,
  };

  editMode: string | null = null;
  editRecord: PurchaseRecord | null = null;

  constructor(private firestore: Firestore) {}

  ngOnInit() {
    const ref = collection(this.firestore, 'purchase_records');
    this.records$ = collectionData(ref, { idField: 'id' }) as Observable<
      PurchaseRecord[]
    >;

    this.records$.subscribe((data) =>
      console.log('[DEBUG] Firestore purchase_records =>', data)
    );
  }

  /** 新增 */
  async addRecord() {
    const ref = collection(this.firestore, 'purchase_records');
    await addDoc(ref, {
      ...this.newRecord,
      created_at: serverTimestamp(),
      updated_at: serverTimestamp(),
    });

    // reset
    this.newRecord = {
      client_id: 0,
      product_id: 0,
      quantity: 1,
      amount: 0,
      order_date: null,
      created_at: null,
      updated_at: null,
    };
  }

  /** 刪除 */
  async deleteRecord(recordId: string) {
    const recordDoc = doc(this.firestore, `purchase_records/${recordId}`);
    await deleteDoc(recordDoc);
  }

  /** 進入編輯模式 */
  startEdit(record: PurchaseRecord) {
    this.editMode = record.id || null;
    this.editRecord = { ...record };
  }

  /** 更新 */
  async updateRecord() {
    if (!this.editRecord?.id) return;
    const recordDoc = doc(this.firestore, `purchase_records/${this.editRecord.id}`);
    await updateDoc(recordDoc, {
      ...this.editRecord,
      updated_at: serverTimestamp(),
    });

    this.editMode = null;
    this.editRecord = null;
  }

  /** 取消編輯 */
  cancelEdit() {
    this.editMode = null;
    this.editRecord = null;
  }
}
