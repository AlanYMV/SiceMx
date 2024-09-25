import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PedidoPlaneacionComponent } from './pedido-planeacion.component';

describe('PedidoPlaneacionComponent', () => {
  let component: PedidoPlaneacionComponent;
  let fixture: ComponentFixture<PedidoPlaneacionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PedidoPlaneacionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PedidoPlaneacionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
