import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BookATreatment } from './book-a-treatment';

describe('BookATreatment', () => {
  let component: BookATreatment;
  let fixture: ComponentFixture<BookATreatment>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BookATreatment]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BookATreatment);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
