<template>
  <div>
    <b-alert variant="danger" dismissible>
      {{ message }}
    </b-alert>
  </div>
</template>

<script>
export default {
  props: ['message'],
};
</script>
