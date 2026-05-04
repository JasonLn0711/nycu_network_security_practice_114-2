// vuln.c
// Compile: gcc -o vuln vuln.c -no-pie -fno-stack-protector -fcf-protection=none
// HW - Network Security Practices: Taint Analysis with Triton

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Taint source: pre-initialized to simulate received network/user data
char user_input[64] = "AAAAAAAAAAAAAAAA"; // 16 bytes of input data

char processed[64];  // intermediate buffer
char output_buf[64]; // taint sink

void process_data() {
  int i;
  for (i = 0; i < 16; i++) {
    processed[i] = user_input[i] ^ 0x42;
  }
}

void copy_to_output() { strncpy(output_buf, processed, 16); }

int main() {
  memset(processed, 0, 64);  // clear intermediate buffer
  memset(output_buf, 0, 64); // clear output buffer
  process_data();
  copy_to_output();
  printf("Output: %s\n", output_buf);
  return 0;
}
