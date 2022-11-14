import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TimetableRowComponent } from './timetable-row.component';

describe('TimetableRowComponent', () => {
  let component: TimetableRowComponent;
  let fixture: ComponentFixture<TimetableRowComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TimetableRowComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TimetableRowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
