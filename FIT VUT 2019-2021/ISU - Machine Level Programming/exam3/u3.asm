;--- �kol 3 ---
;
; Naprogramujte funkci 'unsigned char* task23(int N)', kter� vypo��t� Padovanovu 
; posloupnost N 8bitov�ch ��sel bez znam�nka. Funkce m� jako vstupn� parametr
; po�et prvk� posloupnosti v ECX (32bitov� hodnota se znam�nkem) a vrac� v EAX 
; ukazatel na pole, kter� alokujete funkc� 'malloc', a do kter�ho ulo��te
; jednotliv� prvky posloupnosti.
;
; Padovanova posloupnost je definov�na takto:
;
;   P(0) = 1, P(1) = 1, P(2) = 1, P(n) = P(n-2) + P(n-3)
;
; Funkci 'malloc' importujte makrem CEXTERN:
;
;   CEXTERN  malloc
;
; Funkce 'malloc' je definov�na takto: 
;
;   void* malloc(size_t N)
;     * N je po�et byt�, kter� maj� b�t alokov�ny (32bitov� ��slo bez znam�nka)
;     * funkce vrac� v EAX ukazatel (32bitov� ��slo bez znam�nka)
;     * funkce m��e zm�nit obsah registr� ECX a EDX
;
; Vstup:
;   * ECX = po�et prvk� pole (32bitov� ��slo se znam�nkem)
;
; V�stup:
;   * EAX = 0, pokud bude N <= 0 (tj. nic nealokujete a vr�t�te hodnotu EAX = NULL = 0),
;   * jinak v EAX vr�t�te ukazatel na pole 8bitov�ch prvk� bez znam�nka reprezentuj�c�ch Padovanovu posloupnost
;
; D�le�it�:
;   * Funkce mus� zachovat obsah v�ech registr�, krom� registru EAX a p��znakov�ho registru.
;   * Funkce 'malloc' m��e zm�nit obsah registr� ECX a EDX => pokud je pou��v�te, schovejte si je.
;
; Hodnocen�: a� 6 b.
;

task23:
    push ebp
    mov ebp, esp
    push ecx
    push eax  
    push edx
    xor eax, eax  
    CEXTERN  malloc
  
    mov eax, 0
    mov ecx, [ebp + 8] ;ecx = param N
    
    cmp ecx, 0 ; N<=0
    jl end
    cmp ecx, 1 ;vysledok = 1, ukonci rekurziu
    je one
    
    push dword ecx
    call malloc
    add esp, 4
    ;mov [buffer], eax
    
    dec ecx ; inak rekurzivne volanie funkcie s n-1
    call task23 
    
  one:
    mov eax, 1
    
  end:   
    pop edx 
    pop eax
    pop ecx
    pop ebp
    ret
