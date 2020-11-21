; Naprogramujte funkci, kter� v poli 32bitov�ch ��sel bez znam�nka pA nalezne minimum a vr�t� jeho hodnotu
; v registru EAX. D�lka pole je d�na parametrem N.
;
; Funkci jsou p�ed�v�ny parametry na z�sobn�ku v po�ad� od posledn�ho k prvn�mu (zprava doleva), parametry ze 
; z�sobn�ku ukl�z� volaj�c� a v�sledek funkce se vrac� v registru EAX (konvence jazyka C).
;
; unsigned int task22(const unsigned int *pA, int N)
;
; Vstup:
;   pA: ukazatel na za��tek pole 32bitov�ch prvk� bez znam�nka
;    N: po�et prvk� pole pA (32bitov� ��slo se znam�nkem)
;
; V�stup:
;   EAX = 0, kdy� je pA neplatn� ukazatel (tj. pA == 0) nebo N <= 0
;   EAX = hodnota 32bitov�ho minima bez znam�nka.
;
; D�le�it�:
;   Funkce mus� zachovat obsah v�ech registr�, krom� registru EAX a p��znakov�ho registru.
;
%include "rw32-2018.inc"
section .data
    pA dd 12, 23, 42, 1, 0, 52, -1, 129
    N dd 22
section .text
_main:
    push ebp
    mov ebp, esp
    
    mov ecx, [N]
    mov esi, pA
    
    push ecx
    push esi
    
    call findMin
    call WriteInt32 
         
    pop esi 
    pop ecx                    
    pop ebp
    ret
  
findMin:
    push ebp
    mov ebp, esp
    
    push ecx
    push ebx
    xor ecx, ecx
    xor ebx, ebx
    
    mov ebx, [ebp+8] ;ebx = pA
    mov ecx, [ebp+12];ecx = N
    
    mov eax, 0
    cmp ebx, 0 ;pA == 0
    je end
    cmp ecx, 0 ;pA < 0
    jb end
    mov eax,[ebx+ecx*4]
    
  for:
    dec ecx
    cmp eax, [ebx+ecx*4]
    jb forend
    mov eax, 129
  
  forend:
    cmp ecx, 0
    je end
    jmp for
    
  end:
    pop ebx
    pop ecx
    pop ebp
    ret