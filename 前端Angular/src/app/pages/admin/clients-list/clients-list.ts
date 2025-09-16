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
  serverTimestamp,
} from '@angular/fire/firestore';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http'; // ✅ 新增

interface Client {
  id?: string;
  uid?: string;
  name: string;
  email: string;
  photoURL?: string;
  createdAt?: any; // Firestore Timestamp
  updatedAt?: any; // 新增，用於紀錄最後更新時間
}

@Component({
  selector: 'app-clients-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './clients-list.html',
  styleUrls: ['./clients-list.css'],
})
export class ClientsListComponent implements OnInit {
  clients$!: Observable<Client[]>;

  // 新增用
  newClient: Client = {
    name: '',
    email: '',
    photoURL: '',
    createdAt: null,
    updatedAt: null,
  };

  // 編輯用
  editMode: string | null = null;
  editClient: Client | null = null;

  constructor(private firestore: Firestore, private http: HttpClient) {} // ✅ 加上 HttpClient

  ngOnInit() {
    const ref = collection(this.firestore, 'clients');
    this.clients$ = collectionData(ref, { idField: 'id' }) as Observable<
      Client[]
    >;

    this.clients$.subscribe((data) => {
      console.log('[DEBUG] Firestore clients =>', data);
    });
  }

  /** 新增客戶 */
  async addClient() {
    if (!this.newClient.name || !this.newClient.email) return;

    const ref = collection(this.firestore, 'clients');
    await addDoc(ref, {
      ...this.newClient,
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
    });

    // reset form
    this.newClient = {
      name: '',
      email: '',
      photoURL: '',
      createdAt: null,
      updatedAt: null,
    };
  }

  /** 刪除客戶 */
  async deleteClient(clientId: string) {
    const clientDoc = doc(this.firestore, `clients/${clientId}`);
    await deleteDoc(clientDoc);
  }

  /** 進入編輯模式 */
  startEdit(client: Client) {
    this.editMode = client.id || null;
    this.editClient = { ...client };
  }

  /** 更新客戶 */
  async updateClient() {
    if (!this.editClient?.id) return;
    const clientDoc = doc(this.firestore, `clients/${this.editClient.id}`);
    await updateDoc(clientDoc, {
      ...this.editClient,
      updatedAt: serverTimestamp(),
    });

    this.editMode = null;
    this.editClient = null;
  }

  /** 取消編輯 */
  cancelEdit() {
    this.editMode = null;
    this.editClient = null;
  }

  /** ✅ 指派膚質檢測結果給客戶 */
  assignSkinResult(clientId: string) {
    const latestResult = localStorage.getItem('latestSkinResult');
    if (!latestResult) {
      alert('⚠️ 請先完成膚質檢測！');
      return;
    }

    const parsed = JSON.parse(latestResult);
    const payload = {
      client_id: clientId,
      oil_label: parsed.oil_label,
      oil_prob: parsed.oil_prob,
      sensi_label: parsed.sensi_label,
      sensi_prob: parsed.sensi_prob,
    };

    this.http.post('http://localhost:8000/skintest/save_result', payload)
      .subscribe({
        next: () => alert(`✅ 已將膚質結果寫入客戶 ${clientId}`),
        error: (err) => console.error('❌ 寫入失敗:', err),
      });
  }
}
