<template>
  <v-combobox
    :value="value"
    :items="types"
    @input="input($event)"
  />
</template>

<script>
export default {
  name: 'RRSetType',
  props: {
    value: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    types: [
      'A',
      'AAAA',
      'MX',
      'CNAME',
      'TXT',
      'SPF',
      'CAA',
      'TLSA',
      'OPENPGPKEY',
      'PTR',
      'SRV',
      'DS',
      'DNSKEY',
    ],
  }),
  methods: {
    input(event) {
      this.$emit('input', event);
    },
  },
};
</script>

<style>

</style>
