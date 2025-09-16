import { Component, inject } from '@angular/core';
import { CommonModule, DatePipe, NgFor } from '@angular/common';
import { Firestore, collection, collectionData } from '@angular/fire/firestore';
import { Observable } from 'rxjs';

interface Booking {
  id?: string;
  date?: string;
  time?: string;
  treatment?: string;
  userId?: string;
  createdAt?: any;
}

@Component({
  selector: 'app-bookings-list',
  standalone: true,
  imports: [CommonModule, NgFor, DatePipe],
  templateUrl: './bookings-list.html',
  styleUrls: ['./bookings-list.css'],
})
export class BookingsListComponent {
  private fs = inject(Firestore);
  bookings$: Observable<Booking[]>;

  constructor() {
    const colRef = collection(this.fs, 'bookings');
    this.bookings$ = collectionData(colRef, { idField: 'id' }) as Observable<Booking[]>;
  }

  tsToMs(ts?: { seconds: number }) {
    return ts?.seconds ? ts.seconds * 1000 : null;
  }
}
