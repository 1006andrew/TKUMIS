import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SkinTestComponent } from './skin-test';

describe('SkinTest', () => {
  let component: SkinTestComponent;
  let fixture: ComponentFixture<SkinTestComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SkinTestComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SkinTestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
