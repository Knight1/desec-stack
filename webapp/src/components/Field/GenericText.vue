<template>
  <v-text-field
    :value="value"
    placeholder="(empty)"
    @input="input($event)"
  />
</template>

<script>
export default {
  name: 'GenericText',
  props: {
    value: {
      type: String,
      required: true,
    },
  },
  methods: {
    input(event) {
      this.$emit('input', event);
    },
  },
};
</script>
