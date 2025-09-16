import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Therapy } from './therapy';

describe('Therapy', () => {
  let component: Therapy;
  let fixture: ComponentFixture<Therapy>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Therapy]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Therapy);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
